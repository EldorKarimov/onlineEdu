from django import forms
from django.core.validators import MinValueValidator

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=5)