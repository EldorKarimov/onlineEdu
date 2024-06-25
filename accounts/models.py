from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import UserManager
from .utils import phone_validator
from config.settings import BASE_DIR
from ckeditor.fields import RichTextField

class User(PermissionsMixin, AbstractBaseUser):
    USER_TYPE = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher')
    )
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    patronymic = models.CharField(_("patronymic"), max_length=50)
    bio = RichTextField(_("bio"), null=True, blank=True)
    image = models.ImageField(upload_to='media/users/', verbose_name=_("Image"),
                              default=str(BASE_DIR) + '/static/assets/images/teacher/teacher__1.png',
                              null=True, blank=True)
    
    phone = models.CharField(_("phone"), max_length=13, unique=True, validators=[phone_validator])
    email = models.EmailField(_("email"), unique=True, null=True, blank=True)
    user_type = models.CharField(_("user type"), max_length=8, choices=USER_TYPE, default='STUDENT')
    
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'phone'
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"