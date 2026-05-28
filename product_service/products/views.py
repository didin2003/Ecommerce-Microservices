from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"}, status=200)
    
# ✅ PUBLIC: anyone can view products
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# ✅ PUBLIC: view single product
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


# 🔐 CREATE PRODUCT (protected)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])

def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# 🔐 UPDATE PRODUCT
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])

def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


#  DELETE PRODUCT
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])

def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    product.delete()
    return Response({"message": "Deleted successfully"}, status=204)