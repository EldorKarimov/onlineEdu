from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import random

from common.models import BaseModel
from main.models import Lesson
from accounts.models import User

class MyQuiz(BaseModel):
    QUIZ_TYPE_CHOICES = (
        (1, _("Pre-course assessment")),
        (2, _("Midterm Exam")),
        (3, _("Final Exam")),
        (4, _("Lesson"))
    )

    title = models.CharField(max_length=150, unique=True)
    quiz_pass = models.FloatField(default=60, 
                                    help_text="testdan o'tish foizi")
    duration_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name=_("Duration time"),
        help_text=_("minutes")
    )
    attempts_allowed = models.IntegerField(help_text="Testni necha marta yechishga ruxsat beriladi", verbose_name=_("attemps allowed"))
    number_of_questions = models.IntegerField(default=1, verbose_name=_("number of questions"))
    is_available = models.BooleanField(default=False)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, verbose_name = _("lesson"))
    is_open = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False, verbose_name=_("is started"))
    is_show_selected_ans = models.BooleanField(default=False, verbose_name=_("show selected answers"))
    quiz_type = models.PositiveIntegerField(choices=QUIZ_TYPE_CHOICES, default=4)

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('my_quiz', kwargs={"course_slug": self.lesson.module.course.slug, "quiz_id":self.id})
    
    @property
    def get_questions(self):
        questions = Question.objects.filter(quiz = self, is_available = True)
        questions = list(questions)
        try:
            questions = random.sample(questions, self.number_of_questions)
            return questions
        except Exception as e:
            return None
    
class Question(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    quiz = models.ForeignKey(MyQuiz, on_delete=models.CASCADE)
    is_multiple_choice = models.BooleanField(default=False, verbose_name=_("is multiple choice"))
    is_available = models.BooleanField(default=True, verbose_name=_("is available"))
    mark = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
    @property
    def get_answers(self):
        answers = Answer.objects.filter(question = self)
        answers = list(answers)
        random.shuffle(answers)
        return answers
    
    def get_mark(self, question):
        correct_answers_count = Answer.objects.filter(question = question, is_correct = True).count()
        if correct_answers_count == 0:
            return 1
        mark = self.mark / correct_answers_count
        return mark


class Answer(BaseModel):
    name = models.CharField(max_length=150, verbose_name=_("name"))
    is_correct = models.BooleanField(default=False, verbose_name=_("is correct"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"))

    def __str__(self):
        return self.name
    
class UserAttempt(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    test = models.ForeignKey(MyQuiz, on_delete=models.CASCADE, related_name="user_attempts", verbose_name=_("test"))
    score = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("score"))
    time_taken = models.DurationField(_("time taken"))
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name=_("date taken"))
    is_started = models.BooleanField(default=False, verbose_name=_('is started'))
    is_completed = models.BooleanField(default=False, verbose_name=_('is completed'))

    def __str__(self):
        return f"{self.user.get_full_name()}-{self.test.title}"
    
    @property
    def get_time_taken(self):
        total_seconds = self.time_taken.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes} minut {seconds} sekund"
    
    @property
    def get_total(self):
        total = round(self.score * 100 / self.test.number_of_questions, 2)
        return total

class Result(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(MyQuiz, on_delete=models.SET_NULL, null=True, blank=True)
    total_questions = models.PositiveIntegerField()
    correct_questions = models.DecimalField(max_digits=10, decimal_places=2)
    is_pass = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name}"
    
    @property
    def get_percentage(self):
        return round((self.correct_questions * 100 / self.total_questions), 2)


class UserAnswer(BaseModel):
    attempt = models.ForeignKey(UserAttempt, related_name="user_answers", on_delete=models.CASCADE, verbose_name=_("attempt"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"))
    selected_answers = models.ManyToManyField(Answer, verbose_name=_("selected answers"))

    def __str__(self):
        return f"{self.question.name}-{self.attempt.score}"