from django.urls import path
from .views import add_to_cart, get_cart, remove_from_cart,update_quantity, health_check

urlpatterns = [
    path('', get_cart),
    path('add/', add_to_cart),
    path('remove/<int:id>/', remove_from_cart),
    path('health/', health_check),
    path('update/<int:id>/', update_quantity),
]