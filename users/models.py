from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя с заданным email и паролем."""
        extra_fields.setdefault('is_staff', True)  # Суперпользователь должен быть staff
        extra_fields.setdefault('is_superuser', True)  # Суперпользователь должен быть суперпользователем

        # Проверяем, что is_staff и is_superuser установлены в True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

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

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличными'),
        ('bank_transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_data = models.DateField(verbose_name='дата платежа', help_text='введите дату платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE, related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE, related_name='payment')
    payment_amount = models.PositiveIntegerField(verbose_name='cумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='способ оплаты')

    def __str__(self):
        return f"Payment by {self.user} fot {self.paid_course or self.paid_lesson} on {self.payment_method}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'