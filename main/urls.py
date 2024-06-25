from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('course/<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path("course/lesson/<slug:course_slug>/<slug:module_slug>/<slug:lesson_slug>/", views.LessonDetailView.as_view(), name="lesson_detail"),
]