from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import random

from .models import *

class MyQuizView(LoginRequiredMixin, View):
    def get(self, request, course_slug, quiz_id):
        quiz = get_object_or_404(MyQuiz, id = quiz_id)
        questions = Question.objects.filter(quiz = quiz)
        questions_count = questions.count()
        questions = random.sample(list(questions), len(questions))
        
        context = {
            "questions":questions,
            "quiz":quiz,
            "questions_count": questions_count
        }
        return render(request, "quiz/questions.html", context)

    def post(self, request, course_slug, quiz_id):
        quiz = get_object_or_404(MyQuiz, id = quiz_id)
        questions = Question.objects.filter(quiz = quiz)
        questions = random.sample(list(questions), len(questions))
