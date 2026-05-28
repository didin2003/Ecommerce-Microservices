from django.urls import path
from .views import create_order, create_payment, verify_payment

urlpatterns = [
    path('checkout/', create_order),
    path('pay/<int:order_id>/', create_payment),
    path('verify/', verify_payment),
    path('health/', health_check),
]