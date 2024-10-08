from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, telegram_id, phone, password, **extra_fields):
        if not telegram_id:
            raise ValueError(_("telegram_id number is required"))
        user = self.model(
            phone = phone,
            telegram_id=telegram_id,
            **extra_fields
        )
        user.password = make_password(password=password)
        user.save(using = self._db)
        return user
    def create_superuser(self, telegram_id, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(telegram_id, phone, password, **extra_fields)