from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    @property
    def imageURL(self) -> str:
        try:
            url = self.image.url
        except:
            url = '/images/placeholder.png'
        return url

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=200, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_total_price(self) -> float:
        ordered_items = self.orderitem_set.all()
        total = sum([item.get_total for item in ordered_items])
        return total

    @property
    def get_total_quantity(self) -> int:
        ordered_items = self.orderitem_set.all()
        total = sum([item.quantity for item in ordered_items])
        return total

    def __str__(self) -> str:
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self) -> float:
        total = self.quantity * self.product.price
        return total

    def __str__(self) -> str:
        return str(self.id)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address
