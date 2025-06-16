from django.shortcuts import render
from django.views import View
from .models import About

class AboutView(View):
    def get(self, request):
        about = About.objects.last()
        return render(request, 'common/about.html', {'about':about})