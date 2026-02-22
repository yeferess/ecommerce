from decimal import Decimal
from products.models import Product

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),  # aseguramos que el precio se guarde
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            item = cart[str(product.id)]
            item['product'] = product
            item['price'] = Decimal(item['price'])  #convertimos el string a Decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_subtotal(self):
        total = self.get_total_price()
        subtotal = total / Decimal('1.19')
        return subtotal.quantize(Decimal('0.01')) #dos cifras decimales

    
    def get_iva(self):        
        iva = self.get_subtotal() * Decimal('0.19')
        return iva.quantize(Decimal('0.01'))
    
    def get_discount(self):
        total = self.get_total_price()

        if total >= Decimal('1000000'):
            discount_rate = Decimal('0.10')
        elif total >= Decimal('500000'):
            discount_rate = Decimal('0.05')
        elif total >= Decimal('250000'):
            discount_rate = Decimal('0.03')
        else:
            discount_rate = Decimal('0.00')

        discount_amount = total * discount_rate
        return discount_amount, discount_rate  # devuelve monto y porcentaje

    
    def get_total_after_discount(self):
        total = self.get_total_price()
        discount, _ = self.get_discount()
        return total - discount

    def clear(self):
        del self.session['cart']
        self.save()
