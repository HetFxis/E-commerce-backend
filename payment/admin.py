from django.contrib import admin
from .models import Order

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display=['user','amount','razorpay_order_id']
  