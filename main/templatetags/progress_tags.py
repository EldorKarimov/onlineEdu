from django import template
from main.models import UserLessonProgress

register = template.Library()

@register.simple_tag
def get_user_progress(lesson, user):
    try:
        progress = UserLessonProgress.objects.get(lesson = lesson, user = user)
        return progress
    except:
        return None