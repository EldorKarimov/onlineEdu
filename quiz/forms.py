from django import forms

class QuestionsAddForm(forms.Form):
    questions = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 20,
            'placeholder': """# savol matni
+to'g'ri javob
-javob 2
-javob 3
-javob 4
===
# savol matni
+to'g'ri javob
-javob 2
-javob 3
-javob 4
===
....""",
            'style': 'width:100%; border:1px solid #ccc; border-radius:8px; padding:10px; font-size:14px;'
        })
    )
