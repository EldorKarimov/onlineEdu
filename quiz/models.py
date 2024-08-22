from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from common.models import BaseModel
from main.models import Lesson
from accounts.models import User

class MyQuiz(BaseModel):
    title = models.CharField(max_length=150, unique=True)
    quiz_pass = models.FloatField(default=60, 
                                    help_text="testdan o'tish foizi")
    duration_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name=_("Duration time"),
        help_text=_("minutes")
    )
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, verbose_name = _("lesson"))
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('my_quiz', kwargs={"course_slug": self.lesson.module.course.slug, "quiz_id":self.id})
    
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
    is_pass = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name} - {self.quiz.title}"
    
    @property
    def get_percentage(self):
        return round((self.correct_questions * 100 / self.total_questions), 2)
