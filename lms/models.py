from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название курса",
        help_text="укажите название курса",
    )
    preview = models.ImageField(
        upload_to="lms/preview",
        verbose_name="превью",
        help_text="Загрузите превью курса",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="описание курса", help_text="введите описание курса", **NULLABLE
    )

    def __str__(self):
        return f"Курс {self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название урока",
        help_text="укажите название урока",
        **NULLABLE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
        help_text="укажите курс",
    )
    description = models.TextField(
        verbose_name="описание урока", help_text="введите описание урока", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="lms/preview",
        verbose_name="превью",
        help_text="Загрузите превью урока",
        **NULLABLE,
    )
    link_video = models.URLField(
        verbose_name="ccылка на видео", help_text="укажите ссылку на видео", **NULLABLE
    )

    def __str__(self):
        return f"Урок {self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]
