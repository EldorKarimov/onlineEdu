from django.db import models
from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User
from django.urls import reverse

class Course(BaseModel):
    title = models.CharField(_("title"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=150, unique=True)
    description = RichTextUploadingField(_("description"))
    image = models.ImageField(_("image"), upload_to='media/course/images', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ])
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    @property
    def get_course_duration(self):
        modules = self.module_set.all()
        minutes = 0
        hours = 0
        seconds = 0
        for module in modules:
            hours += module.get_total_duration.get('hours')
            minutes += module.get_total_duration.get('minutes')
            seconds += module.get_total_duration.get('seconds')
        hours = hours + (minutes + seconds // 60) // 60
        minutes = (minutes + seconds // 60) % 60
        seconds = seconds % 60
        return {"hours":hours, "minutes": minutes, "seconds": seconds}
    
    @property
    def get_hours(self):
        return self.get_course_duration.get('hours')

    @property
    def get_minutes(self):
        return self.get_course_duration.get("minutes")


    def get_link(self):
        return reverse('main:course_detail', kwargs={'course_slug': self.slug})
    
    def get_lessons_count(self):
        modules = Module.objects.filter(course = self)
        lesson_count = 0
        for module in modules:
            lesson_count += Lesson.objects.filter(module = module).count()
        return lesson_count

    def get_enrolled_users_count(self):
        """Returns the number of users enrolled in a course"""
        return UserLessonProgress.objects.filter(course=self).values('user').distinct().count()
    
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

class Module(BaseModel):
    name = models.CharField(_("name"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=150, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("course"))

    def __str__(self):
        return self.name
    
    @property
    def get_total_duration(self):
        lessons = self.lesson_set.all()
        minutes = 0
        hours = 0
        seconds = 0
        for lesson in lessons:
            minutes += lesson.minutes
            seconds += lesson.seconds
        hours = (minutes + seconds // 60) // 60
        minutes = (minutes + seconds // 60) % 60
        seconds = seconds % 60
        return {"hours":hours, "minutes": minutes, "seconds": seconds}
    
    @property
    def get_hour(self):
        return self.get_total_duration.get('hours')
    
    @property
    def get_minute(self):
        return self.get_total_duration.get('minutes')
    
    @property
    def get_second(self):
        return self.get_total_duration.get('seconds')

    
    class Meta:
        verbose_name = _("module")
        verbose_name_plural = _("modules")

class Lesson(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name=_('module'))
    title = models.CharField(_("title"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=150, unique=True)
    video_link = models.URLField(_("video link"), validators=[URLValidator])
    minutes = models.IntegerField(_("minutes"), validators=[MinValueValidator(1), MaxValueValidator(60)])
    seconds = models.PositiveIntegerField(_("seconds"), validators=[MinValueValidator(0), MaxValueValidator(59)])
    content = RichTextUploadingField(_("content"), null=True, blank=True)
    is_open = models.BooleanField(_("open"), default=False)
    is_completed = models.BooleanField(_('completed'), default=False)

    def __str__(self):
        return self.title
    
    def get_link(self):
        return reverse('main:lesson_detail', kwargs={'lesson_slug':self.slug, 'module_slug': self.module.slug, 'course_slug':self.module.course.slug})
    
class FileLesson(BaseModel):
    name = models.CharField(_('file name'), max_length=50)
    file = models.FileField(_('file'), validators=[
        FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'ppt', 'pptx'])
    ])
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, related_name="file_lessons_by_module", verbose_name="module")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserLessonProgress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=_("lesson"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("course"))
    is_completed = models.BooleanField(_("completed"), default=False)
    is_open = models.BooleanField(_("open"), default=False)

    class Meta:
        unique_together = ('user', 'lesson', 'course')
    
    def __str__(self):
        return f"{self.user} - {self.lesson.title}"
    
class QuestionAnswer(BaseModel):
    class QAType(models.TextChoices):
        QUESTION = "question", "Question"
        ANSWER = "answer", "Answer"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    file = models.FileField(upload_to='uploads/qa/files', validators=[FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'png', 'jpg']
    )], null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    type = models.CharField(max_length=9, choices=QAType.choices)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()
