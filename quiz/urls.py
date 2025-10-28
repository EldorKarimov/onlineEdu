from django.urls import path
from . import views

urlpatterns = [
    path('quiz-list/', views.QuizListView.as_view(), name="quiz_list"),
    path('<slug:course_slug>/<int:quiz_id>/', views.MyQuizView.as_view(), name="my_quiz"),
    path('quiz-details/<slug:course_slug>/<int:quiz_id>/', views.MyQuizDetailView.as_view(), name="quiz_details"),
    path('add/questions/<quiz_id>/', views.CreateQuestionView.as_view(), name='add_questions')
]