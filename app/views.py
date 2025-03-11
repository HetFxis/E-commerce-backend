from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate,get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,Category, Product,Cart,checkout
from .serializer import UserSerializer, LoginSerializer, CategorySerializer, ProductSerializer,CartSerializer,OrderSerializer
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
# import random
# from django.utils.timezone import now
# from django.core.mail import send_mail
# from datetime import timedelta

# class SendOTPView(APIView):
#     """Sends an OTP to the user's email for verification"""

#     def post(self, request):
#         email = request.data.get("email")
#         if not email:
#             return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

#         otp_code = str(random.randint(100000, 999999))  

#         otp_obj, created = OTP.objects.update_or_create(
#         defaults={"otp_code": otp_code},
#          )

#         send_mail(
#             "Your OTP Code",
#             f"Your OTP is {otp_code}. It is valid for 5 minutes.",
#             "your_email@gmail.com",
#             [email],
#             fail_silently=False,
#         )

#         return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)


# class VerifyOTPView(APIView):
#     """Verifies the OTP before allowing signup"""

#     def post(self, request):
#         email = request.data.get("email")
#         otp_code = request.data.get("otp_code")

#         if not email or not otp_code:
#             return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

#         otp_instance = OTP.objects.filter(user__email=email, otp_code=otp_code).first()
#         if otp_instance and otp_instance.is_valid():
#             otp_instance.delete()  # Remove OTP after successful verification
#             return Response({"message": "OTP verified successfully. You can proceed with registration."}, status=status.HTTP_200_OK)

#         return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        # Check OTP validity
        otp_instance = OTP.objects.filter(user__email=email, otp_code=otp_code).first()
        if not otp_instance or not otp_instance.is_valid():
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with user registration
        request.data["password"] = make_password(request.data["password"])
        response = super().create(request, *args, **kwargs)

        otp_instance.delete()  # Remove OTP after successful signup
        return response


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
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]  
    def get_object(self):
        user_id = self.kwargs.get('id', None)
        if user_id:
            return CustomUser.objects.get(id=user_id) 
        else:
            return self.request.user
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
  
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Category_id = self.request.query_params.get('category', None)
        if Category_id:
            return Product.objects.filter(Category_id=Category_id)
        return Product.objects.all()

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
  
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        Category_id = self.request.query_params.get('category', None)
        if Category_id:
            return Product.objects.filter(Category_id=Category_id)
        return Product.objects.all()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

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
