from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name



class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    description = models.CharField(max_length=255)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


    def get_add_to_cart_url(self):
        return reverse("catalogue:add-to-cart", kwargs={
            'id': self.id
        })


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    delivery_address = models.CharField(max_length=255)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total_price = sum([item.get_individual_total for item in orderitems])
        return total_price

    @property
    def get_cart_item_quantity(self):
        orderitems = self.orderitem_set.all()
        total_quantity = sum([item.quantity for item in orderitems])
        return total_quantity

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    @property
    def get_individual_total(self):
        total = self.item.price * self.quantity
        return total

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)

    def __str__(self):
        return f"first line address of order no. {self.id} is {self.address}"
