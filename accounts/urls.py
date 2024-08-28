from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.AuthUserView.as_view(), name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('profile/change/', views.ChangeProfileView.as_view(), name='profile_change')
]