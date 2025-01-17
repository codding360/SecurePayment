from django.urls import path
from .views import PaymentCreateAPIView, PaymentView

urlpatterns = [
    path('create/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('secure/<uuid:payment_id>/', PaymentView.as_view(), name="secure-payment"),
]