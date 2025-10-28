from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.http import HttpResponse
from main.models import *
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from .forms import QuestionsAddForm
from django import http

from .models import *

class QuizListView(LoginRequiredMixin, View):
    def get(self, request):
        tests = MyQuiz.objects.filter(is_available = True)
        context = {
            'tests': tests
        }
        return render(request, 'quiz/quiz-list.html', context)
    
class CreateQuestionView(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        form = QuestionsAddForm()
        return render(request, 'quiz/add-questions.html', {'form':form})
    
    def post(self, request, quiz_id):
        test = get_object_or_404(MyQuiz, id = quiz_id)
        form = QuestionsAddForm(request.POST)
        if form.is_valid():
            questions_data = form.cleaned_data['questions']
            try:
                questions_answers = questions_data.strip().split('===')
                
                for block in questions_answers:  
                    lines = block.strip().split("\n")
                    question_text = lines[0].lstrip('#') 
                    
                    question = Question.objects.create(
                        quiz = test,
                        name = question_text
                    )
                    
                    for line in lines[1:]:
                        is_correct = line.startswith("+")  
                        answer_text = line[1:].strip() 
                        Answer.objects.create(
                            question = question, 
                            name = answer_text,
                            is_correct = is_correct
                        )

                messages.success(request, "Savollar muvaffaqiyatli qo'shildi!")
                return redirect('add_questions', test.id)
            except Exception as e:
                messages.error(request, f"Xato yuz berdi: {e}")
                # return render(request, 'quiz/add-questions.html', {'form':form})
                return http.HttpResponse(form)

class MyQuizDetailView(LoginRequiredMixin, View):
    def get(self, request, course_slug, quiz_id):
        quiz = get_object_or_404(MyQuiz, id = quiz_id)
        results = Result.objects.filter(quiz = quiz, user = request.user)
        context = {
            'quiz':quiz,
            'results':results,
        }
        return render(request, "quiz/quiz-detail.html", context)

class MyQuizView(LoginRequiredMixin, View):
    def get(self, request, course_slug, quiz_id):
        quiz = get_object_or_404(MyQuiz, id = quiz_id)
        questions = quiz.get_questions
        

        if cache.get(f"{request.user.telegram_id}_{quiz.id}_questions") is None:
            cache.set(f"{request.user.telegram_id}_{quiz.id}_questions", questions, timeout=60*quiz.duration_time + 30)
        cached_questions = cache.get(f"{request.user.telegram_id}_{quiz.id}_questions")

        attempt_count = UserAttempt.objects.filter(user = request.user, test = quiz, is_completed = True).count()
        if attempt_count >= quiz.attempts_allowed:
            messages.error(request, f"Testga {quiz.attempts_allowed} marta urinish berilgan sizning urinishingiz tugadi.")
            return redirect('quiz_details', quiz.lesson.module.course.slug, quiz.id)
        
        user_attempt, created = UserAttempt.objects.get_or_create(
            user = request.user,
            test = quiz,
            score = 0,
            time_taken = timezone.timedelta(0),
            is_started = True
        )
        
        context = {
            "questions":cached_questions,
            "quiz":quiz,
            "question_count":len(cached_questions),
        }
        return render(request, "quiz/questions.html", context)

    def post(self, request, course_slug, quiz_id):
        try:
            quiz = get_object_or_404(MyQuiz, id = quiz_id)
            questions = Question.objects.filter(quiz = quiz)
            attempt = UserAttempt.objects.filter(user = request.user, test = quiz, is_completed = False).last()
            with transaction.atomic():
                score = 0
                overall_score = 0
                cached_questions = cache.get(f"{request.user.telegram_id}_{quiz.id}_questions")
                for i in cached_questions:
                    overall_score += i.mark
    

                for question in cached_questions:
                    if question.is_multiple_choice:

                        selected_answer_ids = request.POST.getlist(f"question_{question.id}")
                        
                        if selected_answer_ids:
                            for ans_id in selected_answer_ids:
                                answer = get_object_or_404(Answer, id = int(ans_id))
                                if answer.is_correct:
                                    score += answer.question.get_mark(question=question)

                            user_answer = UserAnswer.objects.create(
                                attempt = attempt,
                                question = question,
                            )
                            user_answer.selected_answers.add(*map(int, selected_answer_ids))
                    else:
                        selected_answer_id = request.POST.get(f"question_{question.id}")
                        if selected_answer_id:
                            answer = get_object_or_404(Answer, id = int(selected_answer_id))
                            if answer.is_correct:
                                score += answer.question.get_mark(question=question)
                            

                            user_answer = UserAnswer.objects.create(
                                attempt = attempt,
                                question = question,
                            )
                            user_answer.selected_answers.add(int(selected_answer_id))
                attempt.is_completed = True
                attempt.time_taken = timezone.now() - attempt.created
                attempt.score = score
                attempt.save()

                
                result = (score / overall_score) * 100
                is_pass = False
                if result >= quiz.quiz_pass:
                    is_pass = True
            if is_pass:
                lesson = Lesson.objects.get(slug = quiz.lesson.slug)
                next_lesson = Lesson.objects.filter(module = lesson.module, id__gt=lesson.id).order_by('id').first()
                if next_lesson:
                    next_progress, created = UserLessonProgress.objects.get_or_create(
                        user = request.user,
                        lesson = next_lesson,
                        course = Course.objects.get(slug = course_slug)
                    )
                    next_progress.is_open = True
                    next_progress.save()

            Result.objects.create(
                user = request.user,
                quiz = quiz,
                total_questions = len(cached_questions),
                correct_questions = score,
                is_pass = is_pass
            )
            cache.delete(f"{request.user.telegram_id}_{quiz.id}_questions")
            return redirect('quiz_details', quiz.lesson.module.course.slug, quiz.id)
        except Exception as e:
            raise Exception(f"Xatolik! {e}")