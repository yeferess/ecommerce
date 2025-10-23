from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #muestra solo a usuarios logeados
from .models import Order, OrderItem
from cart.cart import Cart

@login_required # solo usuarios logeados 
def create_order(request):
    cart = Cart(request)

    if request.method == 'POST':        
        order = Order.objects.create(user=request.user) # Crear la orden asociada al usuario logueado, crea la orden en la database

        # Crea los items a partir del carrito
        for item in cart:
            OrderItem.objects.create( # crea cada producto dentro de la orden en la base de datos
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear() # limpia el carrito

        return render(request, 'orders/order_created.html', {'order': order})
    
    return render(request, 'orders/order_create.html', {'cart': cart}) # Si no es POST, muestra el carrito de comproas

@login_required
def profile_orders(request):
    
    orders = Order.objects.filter(user=request.user).order_by('-date_order')#Historial de órdenes del usuario actual
    return render(request, 'orders/order_user.html', {'orders': orders})
