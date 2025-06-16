from django.urls import path
from . import views

app_name = 'common'
urlpatterns = [
    path('', views.AboutView.as_view(), name="about"),
]