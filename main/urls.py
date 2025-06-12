from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('student/dashboard/<str:telegram_id>/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('course/<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path("course/lesson/<slug:course_slug>/<slug:module_slug>/<slug:lesson_slug>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path('qa/admin/', views.QuestionAnswerAdmin.as_view(), name='qaAdmin'),
    path('question/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('answer/to/question/<int:question_id>/', views.AnswerTheQuestion.as_view(), name='answer_to_question'),
    path('rating/', views.RatingView.as_view(), name='rating'),
    path("assignments/<slug:course_slug>/<slug:module_slug>", views.FileLessonView.as_view(), name="assignments")
]