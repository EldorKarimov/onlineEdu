from django.db import models
from common.models import BaseModel
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User

class Course(BaseModel):
    title = models.CharField(_("title"), max_length=150)
    description = RichTextUploadingField(_("description"))
    image = models.ImageField(_("image"), upload_to='media/course/images', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ])
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

class Module(BaseModel):
    name = models.CharField(_("name"), max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("course"))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("module")
        verbose_name_plural = _("modules")

class Lesson(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name=_('module'))
    title = models.CharField(_("title"), max_length=150)
    video_link = models.URLField(_("video link"), validators=[URLValidator])
    minutes = models.IntegerField(_("minutes"), validators=[MinValueValidator(1), MaxValueValidator(60)])
    seconds = models.PositiveIntegerField(_("seconds"), validators=[MinValueValidator(0), MaxValueValidator(59)])
    content = RichTextUploadingField(_("content"), null=True, blank=True)
    is_open = models.BooleanField(_("open"), default=False)
    is_completed = models.BooleanField(_('completed'), default=False)

    def __str__(self):
        return self.title
    
class FileLesson(BaseModel):
    name = models.CharField(_('file name'), max_length=50)
    file = models.FileField(_('file'), validators=[
        FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'ppt', 'pptx'])
    ])
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name