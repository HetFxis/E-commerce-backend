from django.urls import path
from .views import CreateOrderView,VerifyPaymentView,OrderListView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='coffee-payment'),
    path('verify/', VerifyPaymentView.as_view(), name='coffee-payment'),
    path('orders/', OrderListView.as_view(), name='coffee-payment'),
    
]