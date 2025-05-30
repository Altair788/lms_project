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
   git clone https://github.com/Altair788/LMS_online_school.git
   cd LMS_online_school
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
   poetry run celery -A config worker --loglevel=info
   ```

7. Запустите celery-beat для периодических задач:
   ```bash
   poetry run celery -A config beat --loglevel=info
   ```

## Запуск проекта через Docker Compose

### Предварительные требования

- Установленный Docker и Docker Compose
- Файл .env с необходимыми переменными окружения

### Шаги по запуску

1. Убедитесь, что вы находитесь в корневой директории проекта.

2. Создайте файл .env и заполните его необходимыми переменными окружения.

3. Запустите проект:
   ```bash
   docker-compose up -d --build
   ```

4. После успешного запуска, приложение будет доступно по адресу `http://localhost:8000`.

### Запуск отдельных контейнеров

Вы можете запустить отдельные контейнеры с помощью следующих команд:

- Backend: `docker-compose up -d lms-backend`
- Database: `docker-compose up -d lms-db`
- Redis: `docker-compose up -d lms-redis`
- Celery Worker: `docker-compose up -d lms-celery_worker`
- Celery Beat: `docker-compose up -d lms-celery_beat`

### Проверка работоспособности сервисов

- **Django backend**: 
  Откройте `http://localhost:8000/admin/` в браузере.

- **PostgreSQL**: 
  ```bash
  docker exec -it lms-db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
  ```
  Внутри psql выполните `\dt` для просмотра таблиц.

- **Redis**: 
  ```bash
  docker exec -it lms-redis redis-cli ping
  ```
  Должен быть ответ "PONG".

- **Celery Worker**: 
  ```bash
  docker logs lms-celery_worker
  ```
  Проверьте логи на наличие ошибок.

- **Celery Beat**: 
  ```bash
  docker logs lms-celery_beat
  ```
  Проверьте логи на наличие ошибок и запланированных задач.

### Остановка проекта

```bash
docker-compose down
```

Для удаления всех данных:
```bash
docker-compose down -v
```

## Работа с базой данных в контейнере

Для проверки состояния базы данных и выполнения SQL-запросов внутри контейнера, следуйте этим шагам:

1. Войдите в контейнер базы данных:
   ```
   docker exec -it lms-db bash
   ```

2. Подключитесь к PostgreSQL:
   ```
   psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
   ```

3. Внутри PostgreSQL вы можете использовать следующие команды:

   - Показать список всех баз данных: `\l`
   - Показать список всех таблиц в текущей базе данных: `\dt`
   - Показать структуру конкретной таблицы: `\d `
   - Выполнить SQL-запрос: `SELECT * FROM  LIMIT 5;`
   - Показать список пользователей базы данных: `\du`

4. Для выхода из PostgreSQL введите: `\q`

5. Для выхода из контейнера введите: `exit`

## Тестирование

- Общее покрытие тестами: 74%
- Реализованы unit-тесты для проверки CRUD операций и функционала подписки на обновления курса
- Ключевые области с высоким покрытием:
  - Модели и сериализаторы (92-96%)
  - URL-маршрутизация (100%)
  - Административные интерфейсы (100%)
- Использованы инструменты: pytest, coverage
- Настроен CI/CD pipeline для автоматического запуска тестов при каждом push

## Настройка удаленного сервера и деплой

1. Обновите систему:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Установите Docker, следуя [официальной инструкции](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

3. Настройте файрвол:
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   sudo ufw status
   ```

4. Настройте GitHub Secrets в настройках репозитория (Settings -> Secrets and variables -> Actions):
   - Данные базы данных: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
   - Настройки Django: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
   - Доступ к Docker Hub: `DOCKER_HUB_USERNAME`, `DOCKER_HUB_ACCESS_TOKEN`
   - SSH-доступ: `SSH_USER`, `SSH_KEY`, `SERVER_IP`
   - Настройки Celery: `CELERY_BROKER_URL`, `CELERY_BACKEND`
   - Настройки email: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_SSL`, `EMAIL_USE_TLS`
   - API ключи: `STRIPE_API_KEY`, `CUR_API_KEY`

5. Запуск CI/CD:
   - Push изменений в репозиторий автоматически запустит GitHub Actions workflow.
   - Workflow выполнит линтинг, тесты, сборку Docker-образа и деплой на сервер.

6. Проверка деплоя:
   После завершения workflow, приложение должно быть доступно по IP-адресу сервера на порту 80.

## Автор
Telegram @eslobodyanik
