Вот простой и лаконичный README.md для твоего проекта.
Department Management System
REST API для управления структурой подразделений и сотрудниками. Построено на FastAPI, SQLAlchemy 2.0 и PostgreSQL.
Технологии
- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Alembic (Миграции)
- Docker & Docker Compose
- Pytest
Требования
- Docker
- Docker Compose

Запуск приложения
При запуске автоматически соберутся образы, запустится база данных, применятся миграции базы данных и стартует веб-сервер.
Склонируйте репозиторий.
Выполните команду в корне проекта:
```
docker-compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000
Интерактивная документация Swagger: http://localhost:8000/docs
Запуск тестов
Тесты запускаются внутри контейнера приложения. Убедитесь, что контейнеры запущены.
```
docker-compose exec app pytest tests/tests.py
```

Основные эндпоинты
POST /departments/ — создание подразделения
GET /departments/{id} — получение дерева подразделения с сотрудниками
PATCH /departments/{id} — редактирование и перемещение подразделения
DELETE /departments/{id} — удаление (cascade или reassign)
POST /departments/{id}/employees/ — создание сотрудника (если реализовано)
Переменные окружения
Параметры подключения к базе данных жестко заданы в файле docker-compose.yml для упрощения первого запуска.
