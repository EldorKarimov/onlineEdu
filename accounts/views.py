from django.shortcuts import render, redirect
from django.views import View
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse

from accounts.management.commands.run_bot import bot
from .models import User
from .forms import GetCodeForm

class AuthUserView(View):
    def get(self, request):
        form = GetCodeForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        form = GetCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_id = cache.get(code)
            if not user_id:
                messages.error(request, "Kod amal qilish muddati tugagan. Iltimos yangi kod oling")
                return redirect("auth")
            # user = User.objects.filter(phone = user_id.phone).exists()
            data = bot.get_chat(user_id)
            return HttpResponse(data)
        else:
            messages.error(request, "Invalid")
            return redirect('auth')