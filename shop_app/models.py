from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=256)
    full_name = models.CharField(max_length=256)

    def __str__(self):
        return str(self.id) + " - " + self.full_name


class Category(models.Model):
    name = models.CharField(max_length=35)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.name 
    

class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand_name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    discount = models.IntegerField(default=0)
    digital = models.BooleanField(default=False)
    featured_image = models.ImageField(null=True, blank=True)
    # additional_images = 

    def __str__(self):
        return f"{self.name} - {self.category.name} | {self.price}"
    

class Order(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    @property
    def totalCartItems(self):
        items = self.orderitem_set.all()
        total_quantity = sum([x.quantity for x in items] )
        return total_quantity

    @property
    def totalCartPrice(self):
        items = self.orderitem_set.all()
        total_quantity = sum([x.total_price for x in items] )
        return total_quantity

    def __str__(self):
        return f"{self.customer.full_name} - Order ID: {self.id} | {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.order.id} | {self.product.name} ({self.quantity})"
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(to=Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=85)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.customer.full_name} | {self.order.id} | {self.address}"
