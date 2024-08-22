from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *
from quiz.models import MyQuiz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

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
        if UserLessonProgress.objects.filter(course = course).exists():
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
        context = {
            "lesson": lesson,
            "modules": modules,
        }
        return render(request, 'courses/lesson.html', context)

    def post(self, request, course_slug, module_slug, lesson_slug):
        lesson = get_object_or_404(Lesson, slug=lesson_slug, module__slug=module_slug)
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
