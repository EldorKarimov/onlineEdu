from django.shortcuts import render, redirect
from django.views import View
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .utils import generate_code

from accounts.management.commands.run_bot import bot
from .models import User
from .forms import GetCodeForm

class AuthUserView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        code = request.POST.get('code')
        user_id = cache.get(code)
        if not user_id:
            messages.error(request, "Kod amal qilish muddati tugagan. Iltimos yangi kod oling")
            return redirect("auth")
        data = bot.get_chat(user_id)
        contact = cache.get(user_id)
        user = User.objects.filter(phone = contact).exists()
        if user:
            user = User.objects.get(telegram_id = user_id)
            login(request, user)
            return redirect('main:home')
        else:
            if not data.first_name:
                User.objects.create_user(
                first_name = "first name",
                last_name = data.last_name,
                telegram_id = user_id,
                phone = contact,
                password = generate_code()
            )
            elif not data.last_name:
                User.objects.create_user(
                first_name = data.first_name,
                last_name = "last name",
                telegram_id = user_id,
                phone = contact,
                password = generate_code()
            )
            else:
                User.objects.create_user(
                    first_name = data.first_name,
                    last_name = data.last_name,
                    telegram_id = user_id,
                    phone = contact,
                    password = generate_code()
                )
        
        return HttpResponse(contact)
        