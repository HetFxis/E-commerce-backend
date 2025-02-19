from django.urls import path
from .views import (
   RegisterView, LoginView, 
    UserProfileView, 
    CategoryDetailView,
    CategoryListCreateView,
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    CartView,
    OrderView,
    SendOTPView,
    VerifyOTPView
)
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain access & refresh tokens
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify token validity


    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/profile/<int:id>/', UserProfileView.as_view(), name='user-profile-by-id'),  # Specific user's profile
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create', ProductCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:product_id>/', CartView.as_view(), name='cart-delete'),
    path('order/create/', OrderView.as_view(), name='create_order'),
    path('orders/', OrderView.as_view(), name='user_orders'),
    
]