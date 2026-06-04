
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartSerializer

import requests
PRODUCT_SERVICE_URL = "http://products.didin.in/api/products/"
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"}, status=200)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart(request):
    user_id = request.user.id
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    item, created = CartItem.objects.get_or_create(
        user_id=user_id,
        product_id=product_id
    )

    if not created:
        item.quantity += int(quantity)
        item.save()

    return Response({"message": "Added to cart"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user_id = request.user.id
    items = CartItem.objects.filter(user_id=user_id)

    result = []
    total = 0

    for item in items:
        try:
            res = requests.get(
                f"{PRODUCT_SERVICE_URL}{item.product_id}/",
                timeout=3
            )

            if res.status_code == 200:
                product = res.json()
            else:
                product = {"name": "Unavailable", "price": 0}

        except requests.exceptions.RequestException:
            product = {"name": "Unavailable", "price": 0}

        price = float(product.get("price", 0))
        subtotal = price * item.quantity
        total += subtotal

        result.append({
            "id": item.id,
            "product_id": item.product_id,
            "name": product.get("name"),
            "price": price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return Response({
        "items": result,
        "total": total
    })
# ❌ REMOVE ITEM
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, id):
    user_id = request.user.id
    item = CartItem.objects.filter(id=id, user_id=user_id).first()

    if not item:
        return Response({"error": "Not found"}, status=404)

    item.delete()
    return Response({"message": "Removed"})



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quantity(request, id):
    user_id = request.user.id
    action = request.data.get('action')  # "increase" or "decrease"

    item = CartItem.objects.filter(id=id, user_id=user_id).first()

    if not item:
        return Response({"error": "Not found"}, status=404)

    if action == "increase":
        item.quantity += 1

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()
            return Response({"message": "Item removed"})

    item.save()
    return Response({"message": "Quantity updated"})
