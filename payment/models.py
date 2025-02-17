from app.models import CustomUser
from django.db import models


class payorder(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")]) 
    created_at = models.DateTimeField(auto_now_add=True)
