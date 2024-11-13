from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone

#  вариант проверки по одному пользователю
# @shared_task
# def check_last_login(user_id):
#     from .models import User
#
#     user = User.objects.get(id=user_id)
#     last_login = user.last_login
#     if timezone.now() - last_login > timedelta(days=31):
#         print(f"Пользователь '{user.email}' не заходил в систему более месяца.")
#         user.is_active = False
#         user.save()
# from django.db import IntegrityError


# вариант проверки для всех пользователей
@shared_task
def check_last_login():
    User = get_user_model()
    try:
        inactive_users = User.objects.filter(
            last_login__lt=timezone.now() - timedelta(days=30), is_active=True
        )

        for user in inactive_users:
            print(f"Пользователь '{user.email}' не заходил в систему более месяца.")
            user.is_active = False
            print(f"Пользователь '{user.email}' переведен в статус 'неактивный'.")
            user.save()
    except IntegrityError as e:
        print(f"Ошибка при обновлении пользователя: {e}")
