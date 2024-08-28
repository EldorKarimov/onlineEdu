from django import forms
from django.core.validators import MinValueValidator
from .models import User

class GetCodeForm(forms.Form):
    code = forms.CharField(max_length=5)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'image', 'bio')