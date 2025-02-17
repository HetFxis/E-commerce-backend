from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Category, Product,Cart,checkout
from .serializer import UserSerializer, LoginSerializer, CategorySerializer, ProductSerializer,CartSerializer,OrderSerializer

from django.shortcuts import get_object_or_404

# User Management Views
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  
    def get_object(self):
        user_id = self.kwargs.get('id', None)
        if user_id:
            return CustomUser.objects.get(id=user_id) 
        else:
            return self.request.user
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'message': 'Login successful',
                    'userid': user.id
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
  
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Category_id = self.request.query_params.get('category', None)
        if Category_id:
            return Product.objects.filter(Category_id=Category_id)
        return Product.objects.all()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        # Validate product
        product = get_object_or_404(Product, id=product_id)
        print(product)
        total_price = product.price * quantity

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, 
            product=product,
            defaults={'quantity': quantity,'total':total_price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.total = cart_item.quantity * product.price  # Update total price
            cart_item.save()

        return Response(
            {"message": "Product added to cart successfully!"},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, product_id):
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.delete()
        return Response({"message": "Product removed from cart"})
class OrderView(generics.ListCreateAPIView):
    queryset = checkout.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        """Fetch all orders of the authenticated user"""
        
        orders = checkout.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
       
        # Get the user's cart
        cart_items = Cart.objects.filter(user=request.user)
        print(cart_items)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        required_fields = ["full_name", "email", "address", "city", "state", "zip_code"]

        if not all(data.get(field) for field in required_fields):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        total_price = sum(item.total for item in cart_items)

        # Create order
        order =checkout.objects.create(
            user=request.user,
            full_name=data["full_name"],
            email=data["email"],
            address=data["address"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            total_amount=total_price,  # Assuming you have a total_amount field
        )

        # Optionally: Move items from cart to order items
        for item in cart_items:
            order.items.add(item)

        # Clear the cart after order is placed
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

import razorpay
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import checkout
from .serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class CreateRazorpayOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get("amount")  # Amount in Rupees
        amount_paise = int(amount) * 100  # Convert to Paisa

        if amount_paise <= 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Razorpay Client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create order in Razorpay
        razorpay_order = client.order.create(
            {
                "amount": amount_paise,  # Razorpay takes amount in Paisa
                "currency": "INR",
                "payment_capture": 1,  # Auto capture payment
            }
        )

        # Save order in DB
        order = Order.objects.create(
            user=user,
            razorpay_order_id=razorpay_order["id"],
            amount=amount,
            status="Pending"
        )

        return Response(
            {
                "order_id": razorpay_order["id"],
                "amount": razorpay_order["amount"],
                "currency": razorpay_order["currency"],
                "key": settings.RAZORPAY_KEY_ID,
            },
            status=status.HTTP_201_CREATED
        )
