from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.AuthUserView.as_view(), name='auth'),
    path('logout/', views.logout_view, name='logout'),
]