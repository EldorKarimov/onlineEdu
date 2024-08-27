from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http.response import HttpResponse

class AdminLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'TEACHER':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
