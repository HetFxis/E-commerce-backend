from django.contrib import admin
from .models import payorder,Order
@admin.register(payorder)
class pay(admin.ModelAdmin):
    list_display=['id','amount']
@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display=['id','payment_id']
  