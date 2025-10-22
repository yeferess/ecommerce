from django.urls import path
from . import views

app_name = 'products' 

urlpatterns = [
    path('', views.product_list, name='product_list'),  
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('<int:id>/', views.product_detail, name='product_detail'),
]
