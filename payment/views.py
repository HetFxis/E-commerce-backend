import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from rest_framework import status

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is logged in

    def post(self, request):
        try:
            # data = request.data
            amount = request.data.get("amount")  # Amount in paise (₹500 = 50000)
            if not amount:
                return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Create order in Razorpay
            order_data = {
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1",
            }
            razorpay_order = razorpay_client.order.create(data=order_data)

            # Save order in the database
            # order = Order.objects.create(
                # user=request.user,
                # razorpay_order_id=razorpay_order["id"],
                # total_price=amount/100,  # Convert paise to INR
                # status="Pending",
            # )

            print(razorpay_order)
            return Response({
                "razorpay":razorpay_order,
                "order_id": razorpay_order["id"],
                "key": settings.RAZORPAY_KEY_ID
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            razorpay_payment_id = request.data.get("razorpay_payment_id")
            razorpay_order_id =request. data.get("razorpay_order_id")
            razorpay_signature = request.data.get("razorpay_signature")
            print(razorpay_payment_id)
            if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
                return Response({"error": "Missing payment details"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify Payment Signature
            params = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
            razorpay_client.utility.verify_payment_signature(params)

            # Update Order Status
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_id = razorpay_payment_id
            order.status = "Paid"
            order.save()

            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch successful orders for the user"""
        orders = Order.objects.filter(user=request.user, status="Paid").order_by("-created_at")
        order_data = [
            {
                "order_id": order.razorpay_order_id,
                "amount": order.amount,
                "status": order.status,
                "created_at": order.created_at,
            }
            for order in orders
        ]
        return Response(order_data, status=status.HTTP_200_OK)
