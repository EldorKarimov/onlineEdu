from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .utils import generate_code


from accounts.management.commands.run_bot import bot
from .models import User
from .forms import GetCodeForm, UserProfileForm

class AuthUserView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        code = request.POST.get('code')
        user_id = cache.get(code)
        if not user_id:
            messages.error(request, "Kod amal qilish muddati tugagan. Iltimos yangi kod oling")
            return redirect("accounts:auth")
        data = bot.get_chat(user_id)
        contact = cache.get(user_id)
        user = User.objects.filter(telegram_id = user_id).exists()
        if user:
            user = User.objects.get(telegram_id = user_id)
            login(request, user)
            return redirect('main:home')
        else:
            if not data.first_name:
                user = User.objects.create_user(
                first_name = "first name",
                last_name = data.last_name,
                telegram_id = user_id,
                phone = contact,
                password = generate_code()
            )
            elif not data.last_name:
                user = User.objects.create_user(
                first_name = data.first_name,
                last_name = "last name",
                telegram_id = user_id,
                phone = contact,
                password = generate_code()
            )
            else:
                user = User.objects.create_user(
                    first_name = data.first_name,
                    last_name = data.last_name,
                    telegram_id = user_id,
                    phone = contact,
                    password = generate_code()
                )
        login(request, user)
        login_redirect_path = request.GET.get("next", "/")
        return redirect(login_redirect_path)
    
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:home')
    else:
        return HttpResponse("error")
    
class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        profile = get_object_or_404(User, id = request.user.id)
        context = {
            'profile':profile
        }
        return render(request, 'accounts/profile.html', context)

class ChangeProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id = request.user.id)
        form = UserProfileForm(instance=user)
        return render(request, 'accounts/profile_change.html', {'form':form})
    
    def post(self, request):
        user = get_object_or_404(User, id = request.user.id)
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request, 'accounts/profile_change.html', {'form':form})