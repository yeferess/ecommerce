from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required #muestra solo a usuarios logeados
from django.db import transaction
from .models import Order, OrderItem, Invoice
from cart.cart import Cart

@login_required # solo usuarios logeados 
# @transaction.atomic
def create_order(request):
    cart = Cart(request)
    # user=request.user

    if request.method == "GET":
        return render(request, "orders/order_create.html", {"cart": cart})

    if request.method == 'POST':        

        # Crea los items a partir del carrito

        order = Order.objects.create(
            user=request.user,
            discount=cart.get_discount()[0],                # descuento en dinero
            total=cart.get_total_after_discount()           # total con descuento
        )


        for item in cart:             
            #order=order,
            product=item['product']
            price=item['price']
            quantity=item['quantity']
            
        # order = Order.objects.create(user=request.user) # Crear la orden asociada al usuario logueado, crea la orden en la database        

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
        
    invoice = Invoice.objects.create(order=order)
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
    invoice = getattr(order, 'invoice', None)  #related_name y no genera errores si no existe la factura
    return render(request, 'orders/order_created.html', {'order': order, 'invoice': invoice})