from django.conf import settings
from django.db import models
# Create your models here.


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
