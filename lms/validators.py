import re

from rest_framework.serializers import ValidationError


def validate_key_words(value):
    if not re.search(r"youtube\.com", value):
        raise ValidationError("Допускается ссылка только на youtube.com.")
