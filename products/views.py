from django.shortcuts import redirect, render
from .models import Product, Category
from django.shortcuts import render, get_object_or_404

# Create your views here.

def product_list(request):
    products = Product.objects.all()  # obtiene todos los productos
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'category': category,
        'products': products,
        'categories': categories
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

