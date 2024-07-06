import re
import random
from django.core.exceptions import ValidationError
regex = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

def phone_validator(value):
    if re.fullmatch(regex, value):
        return True
    else:
        raise ValidationError("phone number is not valid")
    
def generate_code():
    numbers = [1,2,3,4,5,6,7,8,9,0]
    code = ''.join([str(random.choice(numbers)) for _ in range(5)])
    return code