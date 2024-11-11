from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя с заданным email и паролем."""
        extra_fields.setdefault("is_staff", True)  # Суперпользователь должен быть staff
        extra_fields.setdefault(
            "is_superuser", True
        )  # Суперпользователь должен быть суперпользователем

        # Проверяем, что is_staff и is_superuser установлены в True
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

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
        help_text="укажите телефон",
    )
    city = models.CharField(
        max_length=100, verbose_name="город", **NULLABLE, help_text="укажите ваш город"
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="аватар",
        help_text="Загрузите аватарку",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличными"),
        ("card", "Перевод на счет"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка оплаты"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="покупатель",
        help_text="укажите покупателя",
        **NULLABLE,
    )
    course = models.ForeignKey(
        "lms.Course",
        on_delete=models.CASCADE,
        verbose_name="курс",
        related_name="payment",
        help_text="укажите название курса",
    )

    lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.SET_NULL,
        verbose_name="урок",
        **NULLABLE,
        related_name="payment",
        help_text="укажите название урока",
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name="cумма оплаты", help_text="укажите сумму оплаты"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name="способ оплаты",
        help_text="укажите способ оплаты",
    )

    session_id = models.CharField(
        max_length=255,
        verbose_name="идентификатор сессии",
        help_text="укажите идентификатор сессии",
        **NULLABLE,
    )

    link = models.URLField(
        max_length=400,
        verbose_name="ссылка на оплату",
        help_text="укажите ссылку на оплату",
        **NULLABLE,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        verbose_name="статус оплаты",
        help_text="укажите статус оплаты",
    )

    def __str__(self):
        return f"Оплачено {self.user} за {self.course} на сумму {self.payment_amount}, метод оплаты: {self.payment_method}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
