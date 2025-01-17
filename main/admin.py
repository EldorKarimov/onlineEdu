from django.contrib import admin

from .models import *

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')
    prepopulated_fields = {'slug':('title', )}
    list_filter = ('author', )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'is_open', 'is_completed', 'created', 'updated')
    list_filter = ('module', 'is_open', 'is_completed')
    search_fields = ('title', )
    ordering = ('-created', )
    prepopulated_fields = {'slug':('title', )}
    list_editable = ('is_open', )

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    search_fields = ('name', )
    list_filter = ('course', )
    prepopulated_fields = ({'slug':('name', )})
admin.site.register([FileLesson, UserLessonProgress, QuestionAnswer])