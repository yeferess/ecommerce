from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('mis-ordenes/', views.profile_orders, name='profile_orders'),
    path('created/<int:order_id>/', views.order_created, name='order_created'),
]