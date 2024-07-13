from django.contrib import admin

from .models import *

@admin.register(MyQuiz)
class MyQuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_time', 'lesson')
    search_fields = ('title', )
    ordering = ("-created",)

class AnswerAdmin(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ('name', 'is_correct')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("name", "quiz")
    list_filter = ("quiz", )
    search_fields = ("name", )
    ordering = ("-created", )
    inlines = [AnswerAdmin]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'total_questions', 'correct_questions')
    ordering = ('-correct_questions', )
    list_filter = ("user", "quiz")
    search_fields = ("user__first_name", "user__last_name", "quiz__title")
