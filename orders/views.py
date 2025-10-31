from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #muestra solo a usuarios logeados
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from cart.cart import Cart

@login_required # solo usuarios logeados 
@transaction.atomic
def create_order(request):
    cart = Cart(request)
    # user=request.user

    if request.method == "GET":
        return render(request, "orders/order_create.html", {"cart": cart})

    if request.method == 'POST':        

        # Crea los items a partir del carrito
        for item in cart:             
            #order=order,
            product=item['product']
            price=item['price']
            quantity=item['quantity']
            if not product.is_available(quantity): # si la respuesta es false, entra en funcion @transaction.atomic y no deja crear la orden
                messages.error(request, f"No hay suficiente stock para {product.name}, solo {product.stock} unidades disponibles.")
                return redirect('cart:cart_detail')

        order = Order.objects.create(user=request.user) # Crear la orden asociada al usuario logueado, crea la orden en la database        

        for item in cart:
            product=item['product']
            price=item['price']
            quantity=item['quantity']

            OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            quantity=quantity
            )

        #restar cantidades
        product.stock -= quantity
        product.save()        

    cart.clear() # limpia el carrito
    messages.success(request, "¡Orden creada con éxito!")
    return redirect('orders:order_created', order.id)

       

@login_required
def profile_orders(request):
    
    orders = Order.objects.filter(user=request.user).order_by('-date_order')#Historial de órdenes del usuario actual
    return render(request, 'orders/order_user.html', {'orders': orders})


@login_required
def order_created(request, order_id):
    """
    Muestra la página de confirmación después de crear una orden.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})