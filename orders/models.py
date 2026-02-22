from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models import Max
from decimal import Decimal



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} del usuario {self.user.username}"

    def total(self):        
        return sum(item.costo() for item in self.items.all()) # Suma el costo total de todos los ítems en la orden.    
     
    def get_subtotal(self):
        total = self.total()
        subtotal = total / Decimal('1.19')
        return subtotal.quantize(Decimal('0.01')) #dos cifras decimales

    
    def get_iva(self):        
        iva = self.get_subtotal() * Decimal('0.19')
        return iva.quantize(Decimal('0.01'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def costo(self):        
        return self.price * self.quantity #Retorna el costo total de este producto
    
class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    date_invoice = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura # {self.number} - Orden {self.order.id}"
    
    def save(self, *args, **kwargs):
        if not self.number:
            # Busca el número más alto existente y suma 1
            last_number = Invoice.objects.aggregate(Max('number'))['number__max'] or 0
            self.number = last_number + 1
        super().save(*args, **kwargs)
