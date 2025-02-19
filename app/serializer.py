from rest_framework import serializers
from .models import CustomUser,Product,Category,Cart,checkout,ProductImage
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','mobile_number' ,'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

  
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  
    class Meta:
        model = Product
        fields ='__all__'




class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product_name', 'product_id', 'product_price', 'product_image', 'quantity', 'total', 'created_at', 'updated_at']
        read_only_fields = ['user']
        
class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = checkout
        fields = ['id', 'user', 'product_name', 'product_id', 'product_price']
        read_only_fields = ['user']
        