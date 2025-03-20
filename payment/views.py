import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Order
from rest_framework.generics import ListAPIView
from .models import Order
from .serializer import OrderSerializer

User = get_user_model()
# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderView(APIView):
    """Creates an order and stores all details in the database."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get("amount")  # Amount from frontend
            
            if not amount:
                return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user  # Get the authenticated user
            amount_in_paise = int(amount) * 100  # Convert INR to paise

            order_data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": "1",
            }

            # Create Razorpay order
            try:
                razorpay_order = razorpay_client.order.create(data=order_data)
            except Exception as e:
                return Response({"error": f"Razorpay error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            order = Order.objects.create(
                user=request.user,
                amount=amount,
                razorpay_order_id=razorpay_order.get("id"),
                status="Pending",
            )
            

            return Response({
                "order_id": razorpay_order.get("id"),
                "key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "currency": "INR",
                "status": "Order Created",
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    """Verifies payment and updates the order in the database."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            razorpay_payment_id = request.data.get("razorpay_payment_id")
            razorpay_order_id = request.data.get("razorpay_order_id")
            razorpay_signature = request.data.get("razorpay_signature")

            if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
                return Response({"error": "Missing payment details"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify Razorpay payment signature
            params = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            try:
                razorpay_client.utility.verify_payment_signature(params)
            except razorpay.errors.SignatureVerificationError:
                return Response({"error": "Invalid Payment Signature"}, status=status.HTTP_400_BAD_REQUEST)

            # Update order in database
            try:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id, user=request.user)
                order.razorpay_payment_id = razorpay_payment_id
                order.razorpay_signature = razorpay_signature
                order.status = "Paid"
                order.save()
                return Response({"status": "success", "message": "Payment Verified"}, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
