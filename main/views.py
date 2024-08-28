from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *
from quiz.models import MyQuiz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from common.permissions import AdminLoginRequiredMixin
from common.utils import file_checker

class HomePageView(View):
    def get(self, request):
        context = {}
        courses = Course.objects.all().order_by('-created')
        context.update({
            'courses':courses,
        })
        return render(request, 'home.html', context)

class CourseDetailView(View):
    def get(self, request, course_slug):
        context = {}
        course = get_object_or_404(Course, slug = course_slug)
        modules = Module.objects.filter(course = course)
        is_written_to_course = False
        if UserLessonProgress.objects.filter(user = request.user).exists():
            is_written_to_course = True
        lesson_count = 0
        for module in modules:
            lesson_count += Lesson.objects.filter(module = module).count()
        # modules = Module.objects.filter(course = course)
        context.update({
            'course':course,
            # 'modules': modules,
            'lesson_count':lesson_count,
            "is_written_to_course": is_written_to_course
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
        user_lesson_progress.save()
        try:
            my_quiz = lesson.myquiz
            my_quiz.is_open = True
            my_quiz.save()
            messages.success(request, "Tabriklayman! Testni muvaffaqqiyatli tugatdingiz.")
            return redirect("main:lesson_detail", course_slug, module_slug, lesson_slug)
        except ObjectDoesNotExist:
            messages.success(request, "Tabriklayman! Darsni muvaffaqqiyatli tugatdingiz.")
            next_lesson = Lesson.objects.filter(module__slug = module_slug, id__gt = lesson.id).order_by('id').first()
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