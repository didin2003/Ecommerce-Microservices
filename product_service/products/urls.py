from django.urls import path
from .views import (
    product_list,
    product_detail,
    create_product,
    update_product,
    delete_product,
    health_check
)

urlpatterns = [
    path('', product_list),
    path('<int:id>/', product_detail),

    path('create/', create_product),
    path('<int:id>/update/', update_product),
    path('<int:id>/delete/', delete_product),
    path('health/', health_check),
]