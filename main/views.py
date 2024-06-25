from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

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
        lesson_count = 0
        for module in modules:
            lesson_count += Lesson.objects.filter(module = module).count()
        modules = Module.objects.filter(course = course)
        context.update({
            'course':course,
            'modules': modules,
            'lesson_count':lesson_count
        })
        return render(request, 'courses/course-detail.html', context)
    
class LessonDetailView(LoginRequiredMixin, View):
    def get(self, request, course_slug, module_slug, lesson_slug):
        lesson = get_object_or_404(Lesson, slug = lesson_slug, module__slug = module_slug)
        modules = Module.objects.filter(course__slug = course_slug)
        context = {
            "lesson": lesson,
            "modules": modules
        }
        return render(request, 'courses/lesson.html', context)
