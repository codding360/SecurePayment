from PIL import Image, ImageDraw, ImageFont
import os

import re


def get_card_schema(card_number):
    """
    Determines the schema of a bank card based on its number using regex.

    Args:
        card_number (str): The bank card number as a string.

    Returns:
        str: The card schema (Visa, MasterCard, American Express, or Unknown).
    """
    card_number = card_number.replace(" ", "")  # Remove spaces, if any.

    if not card_number.isdigit():
        return "strip"

    # Visa: Starts with 4, length is 13, 16, or 19
    if re.match(r"^4\d{12}(\d{3})?(\d{3})?$", card_number):
        return "visa"

    # MasterCard: Starts with 51-55 or 2221-2720, length is 16
    if re.match(r"^(5[1-5]\d{14}|2(2[2-9]\d{2}|[3-6]\d{3}|7[01]\d{2}|720\d{2})\d{10})$", card_number):
        return "mastercard"

    # American Express: Starts with 34 or 37, length is 15
    if re.match(r"^3[47]\d{13}$", card_number):
        return "american_express"

    return "strip"