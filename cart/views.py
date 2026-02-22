from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from requests import request
from products.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    discount_amount, discount_rate = cart.get_discount()
    total_after_discount = cart.get_total_after_discount()

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'discount_rate': discount_rate * 100,  # para mostrar %
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
    })

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required
@transaction.atomic
def cart_validate(request):
    cart = Cart(request)

    # Solo valida en POST, cuando el usuario da clic en "Finalizar compra"
    if request.method == "POST":
        for item in cart:
            product = item['product']
            quantity = item['quantity']

            if not product.is_available(quantity):
                messages.error(
                    request,
                    f"No hay suficiente stock para {product.name}. Solo {product.stock} unidades disponibles."
                )
                return redirect('cart:cart_detail')  # vuelve al carrito con mensaje

        
        return redirect('orders:create_order')

    
    return redirect('cart:cart_detail')
