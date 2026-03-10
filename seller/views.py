from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from orders.models import Order
from products.models import Product
from products.form import ProductForm
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from datetime import date

def is_seller(user):
    # return user.groups.filter(name='Vendedor').exists()
    return user.is_authenticated and user.groups.filter(name='Vendedor').exists()

seller_required = user_passes_test(is_seller, login_url='accounts:login')


# @login_required
@seller_required
def dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    low_stock = Product.objects.filter(stock__lte=5).count() #lte Less than or Equal 
    recent_orders = Order.objects.order_by('-date_order')[:10] # el -date_order significa el mas reciente primero
    completed_orders = Order.objects.filter(status='completed').count()

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'low_stock': low_stock,
        'recent_orders': recent_orders,
        'completed_orders': completed_orders
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
    new_status = request.POST.get('status')
    valid = [s[0] for s in Order.STATUS_CHOICES]
    if new_status in valid:
        order.status = new_status
        order.save()
        messages.success(request, f'Estado del pedido #{order.id} actualizado.')
    else:
        messages.error(request, 'Estado inválido.')
    
    # Si viene del detalle, regresa al detalle, sino va al order_list
    referer = request.META.get('HTTP_REFERER', '')  #Obtiene la URL desde donde vino el usuario, pag anterior
    if 'orders/' in referer and str(order_id) in referer:
        return redirect('seller:order_detail', order_id=order.id)
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

@login_required
@seller_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.select_related('product').all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'seller/order_detail.html', context)

@login_required
@seller_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product       
    }
    return render(request, 'seller/product_detail.html', context)

@login_required
@seller_required
def add_product(request):
    
    if request.method == 'POST':      

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)            
            product.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('seller:inventory')
    else:
        form = ProductForm()
        messages.error(request, "Todos todos los campos del formulario son obligatorios!.")
    return render(request, 'seller/add_product.html', {'form': form})        

@login_required
@seller_required
def sales(request):
    from datetime import date
    
    date_start = request.GET.get('date_start', '')
    date_end = request.GET.get('date_end', '')    
    orders = Order.objects.all().order_by('-date_order')
    
    if date_start and date_end:
        orders = orders.filter(date_order__gte=date_start).filter(date_order__lte=date_end).filter(status='completed')
    else:
        orders = orders.filter(date_order__date=date.today()).filter(status='completed')

    total_sales = sum(order.total() for order in orders)
    total_orders = orders.count()

    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'date_start': date_start,
        'date_end': date_end,
    }
    return render(request, 'seller/sales.html', context)