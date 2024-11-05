from datetime import date

from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    """
    Команда для добавления образцов платежей в базу данных.
    """

    def handle(self, *args, **options):
        # Создание тестовых пользователей
        user1 = User.objects.create_user(
            email="user1@example.com",
            password="password123",
            phone="+12345678901",
            city="City1",
        )

        user2 = User.objects.create_user(
            email="user2@example.com",
            password="password123",
            phone="+12345678902",
            city="City2",
        )

        # Создание тестовых курсов и уроков
        course1 = Course.objects.create(
            title="Course 1", description="Description for Course 1"
        )
        lesson1 = Lesson.objects.create(title="Lesson 1", course=course1)
        lesson2 = Lesson.objects.create(title="Lesson 2", course=course1)

        # Список платежей для создания
        payment_list = [
            {
                "user": user1,
                "payment_data": date(2024, 10, 1),
                "paid_course": course1,
                "paid_lesson": None,
                "payment_amount": 5000,
                "payment_method": "cash",
            },
            {
                "user": user2,
                "payment_data": date(2024, 10, 1),
                "paid_course": None,
                "paid_lesson": lesson1,
                "payment_amount": 1000,
                "payment_method": "bank_transfer",
            },
            {
                "user": user2,
                "payment_data": date(2024, 11, 2),
                "paid_course": None,
                "paid_lesson": lesson2,
                "payment_amount": 1000,
                "payment_method": "bank_transfer",
            },
        ]

        # Подготовка списка для пакетного создания
        payments_for_create = []
        for payment_item in payment_list:
            payments_for_create.append(Payment(**payment_item))

        # Пакетное создание платежей в базе данных
        Payment.objects.bulk_create(payments_for_create)

        self.stdout.write(self.style.SUCCESS("Successfully added sample payments"))
