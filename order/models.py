from django.conf import settings
from django.db import models
from product.models import Product

# Create your models here.


class OrderInCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} of {self.user}"

    def get_product_total(self):
        if self.product.discounted_price:
            return self.product.discounted_price * self.quantity
        return self.product.price * self.quantity

    def get_save(self):
        if self.product.discounted_price:
            return (self.product.price * self.quantity)-(self.product.discounted_price * self.quantity)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ManyToManyField(OrderInCart)
    start_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    def get_cart_total(self):
        total = 0
        for order in self.product.all():
            total += order.get_product_total()
        return total


class Address(models.Model):
    ADDRESS_CHOICES = (('HOME', 'Home'),
                       ('OFFICE', 'Office'))
    PAYMENT_CHOICES = (('CREDIT/DEBIT CARD', 'Credit/Debit Cards'),
                       ('NET BANKING', 'Net Banking'),
                       ('UPI', 'UPI'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    mobile_number = models.IntegerField()
    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=50)
    colony = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    state = models.ForeignKey(
        'State', on_delete=models.CASCADE)
    city = models.ForeignKey(
        'City', related_name='city', on_delete=models.CASCADE)
    pin_code = models.IntegerField()
    address_type = models.CharField(choices=ADDRESS_CHOICES, max_length=10)
    default_address = models.BooleanField(default=False)


class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(
        'State', related_name='state', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
