from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.http import HttpResponse

from .models import *

class MyQuizView(LoginRequiredMixin, View):
    def get(self, request, course_slug, quiz_id):
        quiz = get_object_or_404(MyQuiz, id = quiz_id)
        questions = Question.objects.filter(quiz = quiz)
        questions_count = questions.count()
        questions = random.sample(list(questions), len(questions))
        results = Result.objects.filter(quiz = quiz, user = request.user)
        
        context = {
            "questions":questions,
            "quiz":quiz,
            "questions_count": questions_count,
            "results":results
        }
        return render(request, "quiz/questions.html", context)

    def post(self, request, course_slug, quiz_id):
        quiz = get_object_or_404(MyQuiz, id = quiz_id)
        questions = Question.objects.filter(quiz = quiz)
        questions = random.sample(list(questions), len(questions))
        correct_count = 0
        wrong_count = 0
        for question in questions:
            if request.POST.get(str(question.id)) == 'True':
                correct_count += 1
            else:
                wrong_count += 1
        result = (correct_count / len(questions)) * 100
        is_pass = False
        if result >= quiz.quiz_pass:
            is_pass = True
        Result.objects.create(
            user = request.user,
            quiz = quiz,
            total_questions = len(questions),
            correct_questions = correct_count,
            is_pass = is_pass
        )
        return redirect('my_quiz', quiz.lesson.module.course.slug, quiz.id)
        
