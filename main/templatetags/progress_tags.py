from django import template
from main.models import UserLessonProgress
from quiz.models import MyQuiz

register = template.Library()

@register.simple_tag
def get_user_progress(lesson, user):
    try:
        progress = UserLessonProgress.objects.get(lesson = lesson, user = user)
        return progress
    except:
        return None
    
@register.simple_tag
def get_first_quiz():
    quiz = MyQuiz.objects.filter(quiz_type=1).last()
    return quiz