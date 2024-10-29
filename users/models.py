from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="укажите почту"
    )

    phone = PhoneNumberField(
        **NULLABLE,
        unique=True,
        verbose_name="номер телефона",
        help_text="укажите телефон"
    )
    city = models.CharField(
        max_length=100, verbose_name="город", **NULLABLE, help_text="укажите ваш город"
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="аватар",
        help_text="Загрузите аватарку",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
