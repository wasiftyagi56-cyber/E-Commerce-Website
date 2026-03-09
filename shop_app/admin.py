from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, ShippingAddress

# Register your models here.
admin.site.register([Category, Product, Customer, Order, OrderItem, ShippingAddress])