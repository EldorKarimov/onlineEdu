from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AuthUserView.as_view(), name='auth')
]