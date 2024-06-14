import re
from django.core.exceptions import ValidationError
regex = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

def phone_validator(value):
    if re.fullmatch(regex, value):
        return True
    else:
        raise ValidationError("phone number is not valid")