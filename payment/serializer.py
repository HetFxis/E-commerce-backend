from rest_framework import serializers
from app.serializer import UserSerializer
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # ✅ Use the UserSerializer to serialize the user object

    class Meta:
        model = Order
        fields = ['razorpay_payment_id', 'razorpay_order_id', 'amount', 'status', 'created_at', 'user']