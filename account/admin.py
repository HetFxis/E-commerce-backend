from django.contrib import admin
from .models import OTP
# Register your models here.
@admin.register(OTP)
class Otp(admin.ModelAdmin):
    list_display=['email','otp_code']