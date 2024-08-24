from django import forms
from .models import QuestionAnswer

class QuestionAnserForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ('file', 'message')