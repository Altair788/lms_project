import logging
import smtplib
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from lms.models import Course

logger = logging.getLogger(__name__)


@shared_task
def send_update_notification(course_id):
    from .models import Course, Subscription

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        logger.error(f"Курс с ID {course_id} не найден.")
        return

        # Проверка, не прошло ли более 4 часов с последнего изменения курса(доп задание)
    if timezone.now() - course.last_updated < timedelta(hours=4):
        print(
            f"Уведомление не отправлено: курс '{course.title}' обновлялся менее 4 часов назад."
        )
        return

    subscribers = Subscription.objects.filter(course=course)

    for subscriber in subscribers:
        try:
            send_mail(
                subject=f"Обновление курса {course.title}",
                message=f"Курс {course.title} был обновлен.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber.user.email],
                fail_silently=False,
            )
            logger.info(
                f"Отправлено письмо пользователю {subscriber.user.email} о новом курсе."
            )
        # обрабатывает инциденты, когда письмо не доставлено по причине ошибок на стороне пользователя
        except smtplib.SMTPException as e:
            # Обработка ошибки отправки
            logger.error(f"Ошибка отправки почты: {e}")
