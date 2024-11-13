import smtplib

from celery import shared_task

from django.core.mail import send_mail

from config import settings
from lms.models import Course


import logging
logger = logging.getLogger(__name__)

@shared_task
def send_update_notification(course_id):
    from .models import Course, Subscription

    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for subscriber in subscribers:
        try:
            send_mail(
                subject=f'Обновление курса {course.title}',
                message=f'Курс {course.title} был обновлен.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber.user.email],
                fail_silently=False,
            )
            logger.info(f'Отправлено письмо пользователю {subscriber.user.email} о новом курсе.')
        # обрабатывает инциденты, когда письмо не доставлено по причине ошибок на стороне пользователя
        except smtplib.SMTPException as e:
        # Обработка ошибки отправки
            logger.error(f"Ошибка отправки почты: {e}")
