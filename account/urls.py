from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()



urlpatterns = [
    path('',include(router.urls)),
    path('refreshtoken/',RefreshTokenView.as_view(),name='refresh-token'),
    path('send-otp/',SendOTPView.as_view(),name='sendotp'),
    path('verify-otp/',VerifyOTPView.as_view(),name='verifyotp'),
    
]