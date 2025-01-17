import uuid
from django.db import models
from payments.utils import get_card_schema


class Payment(models.Model):
    PAYMENT_STATUSES = [
        ('pending', 'Pending'),
        ('opened', 'Opened'),
        ('succeeded', 'Succeeded'),
        ('canceled', 'Canceled'),
    ]

    ERROR_STATUS = [
        ('wrong_otp', 'The OTP code entered is incorrect.')
    ]
    errors = models.CharField(max_length=255, choices=ERROR_STATUS, default=None, null=True, blank=True)


    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='AED')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUSES, default='pending')
    payment_id = models.UUIDField(null=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    # Card Information2
    cardholder_name = models.CharField(max_length=100, null=True, default="ELiot Alderon")  # Cardholder's name
    card_number = models.CharField(max_length=16, null=True)  # Card number (typically 16 digits)
    card_expiry_date = models.CharField(max_length=5, null=True)  # Expiry date (MM/YY format)
    card_cvv = models.CharField(max_length=3, null=True)  # CVV (3 digits)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

    @property
    def schema(self):
        print(self.card_number, " ", get_card_schema(self.card_number))
        return get_card_schema(card_number=self.card_number)