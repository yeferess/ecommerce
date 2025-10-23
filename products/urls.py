from django.urls import path
from . import views

app_name = 'products' 

urlpatterns = [
    path('', views.product_list, name='product_list'),  
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='product_search'),
]
