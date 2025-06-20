from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *
from quiz.models import MyQuiz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.models import (
    Count, Sum, Avg, ExpressionWrapper,
    DecimalField, IntegerField, F
)
from django.db.models.functions import Cast

from .forms import *
from common.permissions import AdminLoginRequiredMixin
from common.utils import file_checker
from quiz.models import MyQuiz, Result

User = get_user_model()

class HomePageView(View):
    def get(self, request):
        context = {}
        courses = Course.objects.all().order_by('created')
        context.update({
            'courses':courses,
        })
        return render(request, 'home.html', context)
    
class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request, telegram_id):
        user = get_object_or_404(User, telegram_id=telegram_id)
        
        
        results = Result.objects.filter(user=user).order_by('quiz', 'created')
        
        
        seen_quizzes = set()
        first_attempts = []
        
        for result in results:
            if result.quiz_id not in seen_quizzes:
                first_attempts.append(result)
                seen_quizzes.add(result.quiz_id)
        
       
        quiz_labels = [result.quiz.title for result in first_attempts]
        quiz_percentages = [result.get_percentage for result in first_attempts]
        
        context = {
            'student': user,
            'quiz_labels': quiz_labels,
            'quiz_percentages': quiz_percentages,
            'first_attempts': first_attempts,
        }
        
        return render(request, 'student_dashboard.html', context)
    
class RatingView(LoginRequiredMixin, View):
    def get(self, request):
        
        users = User.objects.annotate(
            total_quizzes=Count('result', distinct=True),

            # total_xp: butun son (int)
            total_xp=Cast(
                Sum('result__correct_questions'),
                output_field=IntegerField()
            ),

            # avg_score: 10^-2 aniqlikdagi Decimal
            avg_score=ExpressionWrapper(
                Avg('result__correct_questions') * 100 / Avg('result__total_questions'),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        ).exclude(total_quizzes=0).order_by('-total_xp')
        
        leaderboard = []
        for rank, user in enumerate(users, start=1):
            user_results = Result.objects.filter(user=user)
            
            leaderboard.append({
                'rank': rank,
                'name': user.get_full_name() or user.username,
                'challenges': user.total_quizzes,
                'solved': user.total_quizzes,  # Assuming all taken quizzes were solved
                'total_xp': user.total_xp,
                'avg_score': round(user.avg_score, 2) if user.avg_score else 0,
                'user_obj': user  # For potential additional user data
            })
        
        # Split into top 3 and others
        top_users = leaderboard[:3]
        other_users = leaderboard[3:8]  # Showing next 5 users
        
        context = {
            'top_users': top_users,
            'other_users': other_users,
            'total_users': len(leaderboard)
        }
        
        return render(request, 'rating.html', context)

class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, course_slug):
        context = {}
        course = get_object_or_404(Course, slug = course_slug)
        modules = Module.objects.filter(course = course)
        is_written_to_course = False
        if UserLessonProgress.objects.filter(user = request.user).exists():
            is_written_to_course = True
        # modules = Module.objects.filter(course = course)
        context.update({
            'course':course,
            # 'modules': modules,
            'lesson_count':course.get_lessons_count(),
            "is_written_to_course": is_written_to_course,
            "entrolled_users_count":course.get_enrolled_users_count()
        })
        return render(request, 'courses/course-detail.html', context)
    def post(self, request, course_slug):
        if not request.user.is_authenticated:
            return redirect('login')
        course = get_object_or_404(Course, slug = course_slug)
        module = course.module_set.first()
        lesson = module.lesson_set.first()
        user_lesson_progress = UserLessonProgress.objects.create(
            user = request.user,
            lesson = lesson,
            course = course,
            is_open = True
        )
        messages.success(request, "siz kursga muvaffaqqiyatli yozildingiz.")
        return redirect("main:course_detail", course_slug) 
    
class LessonDetailView(LoginRequiredMixin, View):
    def get(self, request, course_slug, module_slug, lesson_slug):
        lesson = get_object_or_404(Lesson, slug=lesson_slug, module__slug=module_slug)
        modules = Module.objects.filter(course__slug=course_slug)
        try:
            course = Course.objects.get(slug = course_slug)
        except Course.DoesNotExist:
            return HttpResponse("Course not found")
        
        chats = QuestionAnswer.objects.filter(user = request.user, lesson = lesson, to = course.author).order_by('-created')
        form = QuestionAnserForm()
        context = {
            "lesson": lesson,
            "modules": modules,
            'chats':chats,
            "form": form
        }
        return render(request, 'courses/lesson.html', context)

    def post(self, request, course_slug, module_slug, lesson_slug):
        qaPost = request.POST.get("message")
        lesson = get_object_or_404(Lesson, slug=lesson_slug, module__slug=module_slug)
        
        if qaPost:
            try:
                course = Course.objects.get(slug = course_slug)
            except Course.DoesNotExist:
                return HttpResponse("Course not found")
            course_author = course.author

            if course_author is None:
                return HttpResponse("Course author not found", status=400)
            
            form = QuestionAnserForm(request.POST, request.FILES)

            fayl = request.FILES.get('fayl')
            if fayl:
                if not file_checker(fayl.name):
                    raise ValidationError("Fayl kengaytmasi noto'g'ri. Ruxsat etilgan kengaytmalar: pdf, doc, docx, png, jpg.")
            if form.is_valid():
                form_save = form.save(commit=False)
                form_save.user = request.user
                form_save.to = course_author
                form_save.type = QuestionAnswer.QAType.QUESTION
                form_save.lesson = lesson
                form_save.save()
                return redirect("main:lesson_detail", course_slug, module_slug, lesson_slug)
            return render(request, 'courses/lesson.html', {"form":form})

            
        
        user_lesson_progress = UserLessonProgress.objects.get(
            user = request.user,
            lesson = lesson,
            course__slug = course_slug
        )
        user_lesson_progress.is_completed = True
        user_lesson_progress.is_open = True
        user_lesson_progress.save()
        try:
            my_quiz = lesson.myquiz
            my_quiz.is_open = True
            my_quiz.save()
            messages.success(request, "Tabriklayman! Testni muvaffaqqiyatli tugatdingiz.")
            return redirect("main:lesson_detail", course_slug, module_slug, lesson_slug)
        except ObjectDoesNotExist:
            messages.success(request, "Tabriklayman! Darsni muvaffaqqiyatli tugatdingiz.")
            next_lesson = Lesson.objects.filter(module__course__slug = course_slug, id__gt = lesson.id).order_by('id').first()
            if next_lesson:
                next_progress, created = UserLessonProgress.objects.get_or_create(
                    user = request.user,
                    lesson = next_lesson,
                    course = Course.objects.get(slug = course_slug)
                )
                next_progress.is_open = True
                next_progress.save()
            return redirect("main:lesson_detail", course_slug, module_slug, lesson_slug)


class QuestionAnswerAdmin(AdminLoginRequiredMixin, View):
    def get(self, request):
        questions = QuestionAnswer.objects.filter(
            to = request.user, type = QuestionAnswer.QAType.QUESTION,
            is_answered = False
        ).order_by('created')
        answered_questions = QuestionAnswer.objects.filter(to = request.user, type = QuestionAnswer.QAType.ANSWER, is_answered=True).order_by('-created')
        questions_count = questions.count()
        context = {
            'questions':questions,
            'answered_questions':answered_questions,
            'questions_count':questions_count
        }
        return render(request, 'qa.html', context)
    
def delete_question(request, question_id):
    question = get_object_or_404(QuestionAnswer, id = question_id)
    question.delete()
    return redirect('main:qaAdmin')


class AnswerTheQuestion(AdminLoginRequiredMixin, View):
    def get(self, request, question_id):
        question = get_object_or_404(QuestionAnswer, id = question_id)
        form = QuestionAnserForm()
        context = {
            'question':question,
            'form':form
        }
        return render(request, 'answer.html', context)
    
    def post(self, request, question_id):
        question = get_object_or_404(QuestionAnswer, id = question_id)
        form = QuestionAnserForm(request.POST, request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = question.user
            form_save.to = request.user
            form_save.lesson = question.lesson
            form_save.is_answered = True
            form_save.type = QuestionAnswer.QAType.ANSWER
            form_save.save()
            return redirect('main:answer_to_question', question.id)
        return HttpResponse("Bad request")
    

class FileLessonView(LoginRequiredMixin, View):
    def get(self, request, course_slug=None, module_slug=None):
        try:
            assignments = FileLesson.objects.filter(module__slug = module_slug)
            context = {
                "assignments":assignments
            }
            return render(request, "courses/assignments.html", context)
        except Exception as e:
            raise f"Xatolik yuz berdi! {e}"