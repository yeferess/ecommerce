from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from orders.models import Order
from products.models import Product
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

def is_seller(user):
    # return user.groups.filter(name='Vendedor').exists()
    return user.is_authenticated and user.groups.filter(name='Vendedor').exists()

seller_required = user_passes_test(is_seller, login_url='accounts:login')


# @login_required
@seller_required
def dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    low_stock = Product.objects.filter(stock__lte=5).count()
    recent_orders = Order.objects.order_by('-date_order')[:5]

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'low_stock': low_stock,
        'recent_orders': recent_orders,
    }
    return render(request, 'seller/dashboard.html', context)


# @login_required
@seller_required
def order_list(request):
    status_filter = request.GET.get('status', '')
    orders = Order.objects.all().order_by('-date_order')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 20)  # 20 pedidos por página
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'seller/order_list.html', context)


@require_POST
@seller_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = [s[0] for s in Order.STATUS_CHOICES]
        if new_status in valid:
            order.status = new_status
            order.save()
            messages.success(request, f'Estado del pedido #{order.id} actualizado.')
        else:
            messages.error(request, 'Estado inválido.')
    return redirect('seller:order_list')


# @login_required
@seller_required
def inventory(request):
    products = Product.objects.select_related('category').order_by('stock')
    context = {'products': products}
    return render(request, 'seller/inventory.html', context)


@require_POST
@seller_required
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    new_stock = request.POST.get('stock')
    
    
    
    try:
        stock_value = int(new_stock)
        if stock_value < 0: 
            messages.error(request, "El stock no puede ser negativo.")
        else:
            product.stock = stock_value
            product.save()
            messages.success(request, f'Stock de "{product.name}" actualizado.')
    except (ValueError, TypeError):
        messages.error(request, 'Valor de stock inválido.')
    return redirect('seller:inventory')

