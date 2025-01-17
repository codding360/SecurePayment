from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "amount", "currency",
            "cardholder_name", "card_number",
            "card_expiry_date", "card_cvv",
            "payment_id", "status", "created_at",
            "schema"
        ]
        read_only_fields = ["payment_id", "status"]


class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "payment_id", "status", "created_at", "errors"
        ]