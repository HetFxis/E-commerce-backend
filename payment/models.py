from app.models import CustomUser
from django.db import models



class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField()  
    razorpay_order_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.TextField(blank=True, null=True)  # Store Razorpay signature for verification
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending")  
    created_at = models.DateTimeField(auto_now_add=True)

