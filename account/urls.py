from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()



urlpatterns = [
    path('',include(router.urls)),
    path('refreshtoken/',RefreshTokenView.as_view(),name='refresh-token'),
    # path('auth/',include('rest_framework.urls')),
    # path('RegisterUserAPI/logout/', UserViews.as_view({'get': 'logout'}), name='logout'),
]