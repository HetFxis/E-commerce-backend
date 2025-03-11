from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.utils.timezone import now


# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True, help_text="Designates whether the user is a customer.")
    is_admin = models.BooleanField(default=False, help_text="Designates whether the user is an admin.")
    mobile_number = models.CharField(max_length=12,default=0)
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_groups',  
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions', 
        blank=True
    )

    def __str__(self):
        return self.username

  

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  
    description = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"  # Proper plural form in admin
        ordering = ['name']  # Default ordering by name

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=255) 
    description = models.TextField(null=True, blank=True)  
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    stock = models.PositiveIntegerField(default=0)  
    image=models.ImageField(upload_to='image', blank=True, null=True)
    sizes = models.JSONField(null=True, blank=True)
    brand= models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    review = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.name
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"Image for {self.product.name}"
class Cart(models.Model):  
    user=models.ForeignKey(CustomUser, related_name="cart", on_delete=models.CASCADE, null=True, blank=True)   
    product=models.ForeignKey(Product, related_name="product_cart", on_delete=models.CASCADE, null=True, blank=True) 
    number_of_items = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)  # Default should be Decimal
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    def __str__(self):
        return f"User: {self.user}, items in cart {self.number_of_items}"


class checkout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="order_cart")
    total_price=models.DecimalField(default=Decimal('0.00'),max_digits=10,decimal_places=2)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Order {self.id} - Rs {self.total_price}"