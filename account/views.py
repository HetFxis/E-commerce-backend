from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
import jwt,datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
# Create your views here.
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