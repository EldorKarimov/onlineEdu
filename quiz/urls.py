from django.urls import path
from . import views

urlpatterns = [
    path('<slug:course_slug>/<int:quiz_id>/', views.MyQuizView.as_view(), name="my_quiz"),
    path('quiz-details/<slug:course_slug>/<int:quiz_id>/', views.MyQuizDetailView.as_view(), name="quiz_details")
]