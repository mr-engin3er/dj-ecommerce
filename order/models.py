from django.conf import settings
from django.db import models
from user.models import Address
from product.models import Product
from payment.models import Coupon, Payment

# Create your models here.


class ProductInCart(models.Model):
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
    order_id = models.CharField(
        max_length=16, unique=True, blank=True, null=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ManyToManyField(ProductInCart)
    start_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(
        Address, related_name="shipping_address", on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        Address, related_name="billing_address", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    ordered_date = models.DateTimeField()
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    in_transist = models.BooleanField(default=False)
    out_for_delivery = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    def get_cart_total(self):
        total = 0
        for order in self.product.all():
            total += order.get_product_total()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def stripe_price(self):
        return int(self.get_cart_total() * 100)


class ReturnOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.pk}"
