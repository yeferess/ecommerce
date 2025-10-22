from django.contrib import admin
from .models import Product, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price','stock', 'category')
    search_fields = ('name', 'description')
    list_filter = ['category']
    ordering = ['name']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Inventario y precio', {
            'fields': ('price', 'stock')
        }),
    )