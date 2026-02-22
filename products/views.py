from django.shortcuts import redirect, render
from .models import Product, Category
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

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

def search_products_ajax(request):
    """AJAX search view - returns JSON for dropdown"""
    query = request.GET.get('q', '')
    results = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)  # si category es FK a Category
        )[:10]  # limitar para dropdown

        for p in products:
            image_url = None
            try:
                if p.image:
                    image_url = request.build_absolute_uri(p.image.url)
            except Exception:
                image_url = None

            results.append({
                'id': p.id,
                'name': p.name,
                'description': (p.description or '')[:120],
                'price': str(p.price),
                'image': image_url
            })

    return JsonResponse({'products': results})

def search_results(request):
    """Full page search results"""
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()
    
    context = {
        'products': products,
        'query': query,
        'total': products.count()
    }
    return render(request, 'products/search_results.html', context)

   