from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
# Create your views here.
from django.contrib.auth.hashers import make_password
from rest_framework import  permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  OTP
import random
from django.core.mail import send_mail
from django.conf import settings
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            # print("hi")
            
            refresh_token = request.data['refresh_token']
            # print("refresht",refresh_token)
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            # print("token",access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  


class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_code = str(random.randint(100000, 999999))  # Generate 6-digit OTP

        # Save OTP (Update if already exists)
        # Send OTP Email
        subject = "Your OTP Code"
        message = f"Your OTP code is {otp_code}. It expires in 10 minutes."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        OTP.objects.filter(email=email).delete()
        OTP.objects.create(email=email, otp_code=otp_code)

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": "Failed to send email. Check email settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp")

        otp_instance = OTP.objects.filter(email=email, otp_code=otp_code).first()
        if not otp_instance:
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        otp_instance.delete()  # OTP should be used only once
        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)

