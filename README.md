
# Платформа для онлайн-обучения

## Описание проекта

Данный проект представляет собой платформу для онлайн-обучения, где пользователи могут размещать свои курсы и материалы. Проект реализован с использованием Django и Django REST Framework (DRF), что позволяет создать мощный бэкенд-сервер, предоставляющий API для взаимодействия с клиентами.

## Основные функции

- **Регистрация и авторизация пользователей**: Пользователи могут регистрироваться и авторизовываться с помощью email. Реализована JWT-авторизация для безопасного доступа к API.
  
- **Управление курсами и уроками**:
  - Модели для курсов и уроков с соответствующими полями (название, описание, превью, ссылки на видео).
  - CRUD операции для управления курсами и уроками с использованием ViewSets и Generic-классов.
  
- **Документация API**: Подключена библиотека [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) для автоматической генерации документации API. Каждый эндпоинт описан в документации, доступной по адресу `/swagger/` или `/redoc/`.

- **Платежная система**: Интеграция с [Stripe](https://stripe.com/docs/api) для обработки платежей за курсы. Реализованы эндпоинты для создания продуктов, цен и сессий оплаты.

- **Подписка на обновления курсов**: Пользователи могут подписываться на обновления курсов. Реализована асинхронная рассылка уведомлений о новых материалах через Celery.

- **Периодическая задача блокировки пользователей**: Фоновая задача, проверяющая дату последнего входа пользователей (`last_login`). Если пользователь не заходил более месяца, его статус `is_active` устанавливается в `False`.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <https://github.com/Altair788/LMS_online_school.git>
   cd <LMS_online_school>
   ```

2. Установите Poetry, если он еще не установлен:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Установите зависимости проекта:
   ```bash
   poetry install
   ```

4. Настройте переменные окружения для Redis и Stripe.

5. Запустите сервер:
   ```bash
   poetry run python manage.py runserver
   ```

6. Запустите Celery worker:
   ```bash
   poetry run celery -A <имя_проекта> worker --loglevel=info
   ```

7. Запустите celery-beat для периодических задач:
   ```bash
   poetry run celery -A <имя_проекта> beat --loglevel=info
   ```

## Тестирование

Проект включает тесты для проверки корректности работы CRUD операций и функционала подписки на обновления курса. Используйте метод `setUp` для заполнения базы данных тестовыми данными.
