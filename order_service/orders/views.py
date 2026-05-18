from django.shortcuts import render
import requests
import hmac
import hashlib
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .razorpay_client import client


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    token = request.headers.get("Authorization")

    res = requests.get(
        "http://127.0.0.1:8003/api/cart/",
        headers={"Authorization": token},
        timeout=5
    )

    if res.status_code != 200:
        return Response({"error": "Cart service failed"}, status=500)

    cart = res.json()
    if isinstance(cart, dict):
        cart = cart.get("items", [])

    if not cart:
        return Response({"error": "Cart is empty"}, status=400)

    order = Order.objects.create(
        user_id=request.user.id,
        total_price=0,
        status="PENDING"
    )

    total = 0
    for item in cart:
        price = float(item.get("price", 0))
        qty = int(item.get("quantity", 0))
        subtotal = price * qty
        total += subtotal

        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            product_name=item["name"],
            price=price,
            quantity=qty,
            subtotal=subtotal
        )

    order.total_price = total
    order.save()

    return Response({
        "message": "Checkout success",
        "order_id": order.id,
        "total": total
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user_id=request.user.id)  
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    if not order.total_price:
        return Response({"error": "Order has no total_price"}, status=400)

    amount = int(float(order.total_price) * 100)

    try:
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    return Response({
        "key": settings.RAZORPAY_KEY_ID,  
        "order_id": razorpay_order["id"],
        "amount": amount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    data = request.data

    razorpay_order_id = data.get("razorpay_order_id")
    razorpay_payment_id = data.get("razorpay_payment_id")
    razorpay_signature = data.get("razorpay_signature")

    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        return Response({"error": "Missing payment fields"}, status=400)

    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    generated_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),  
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature == razorpay_signature:
        order.payment_status = "PAID"
        order.status = "CONFIRMED"
        order.save()
        return Response({"message": "Payment successful"})

    return Response({"error": "Invalid signature"}, status=400)