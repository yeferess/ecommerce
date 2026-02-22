from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/<int:product_id>/stock/', views.update_stock, name='update_stock'),
]