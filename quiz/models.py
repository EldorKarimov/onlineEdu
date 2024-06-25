from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from main.models import Lesson
from accounts.models import User

class MyQuiz(BaseModel):
    title = models.CharField(max_length=150, unique=True)
    duration_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name=_("Duration time")
    )
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, verbose_name = _("lesson"))

    def __str__(self):
        return self.title
    
class Question(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    quiz = models.ForeignKey(MyQuiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Answer(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"))

    def __str__(self):
        return self.name

class Result(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(MyQuiz, on_delete=models.SET_NULL, null=True, blank=True)
    total_questions = models.PositiveIntegerField()
    correct_questions = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.get_full_name} - {self.quiz.title}"
