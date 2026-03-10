from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/<int:product_id>/stock/', views.update_stock, name='update_stock'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('addproduct/', views.add_product, name='add_product'),
    path('sales/', views.sales, name='sales'),

]