from django.urls import path
from .views import CreateOrderView,VerifyPaymentView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='coffee-payment'),
    path('verify/', VerifyPaymentView.as_view(), name='coffee-payment'),
]