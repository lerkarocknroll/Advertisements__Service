# Сервис объявлений (Advertisements Service)

Сервис для создания, просмотра, обновления, удаления и поиска объявлений о купле-продаже. Реализован на FastAPI с использованием PostgreSQL и Docker.

## Функциональность

- Создание объявления: POST /advertisement
- Получение объявления по ID: GET /advertisement/{id}
- Обновление объявления: PATCH /advertisement/{id}
- Удаление объявления: DELETE /advertisement/{id}
- Поиск объявлений с фильтрацией: GET /advertisement?title=...&price_min=...&price_max=...&author=...&skip=...&limit=...

### Поля объявления

| Поле         | Тип      | Обязательное | Описание                      |
|--------------|----------|--------------|-------------------------------|
| title      | string   | да           | Заголовок объявления          |
| description| string   | нет          | Описание                      |
| price      | float    | да           | Цена                          |
| author     | string   | да           | Автор объявления              |
| created_at | datetime | авто         | Дата создания (устанавливается автоматически) |

## Технологии

- Python 3.11
- FastAPI — веб-фреймворк
- SQLAlchemy 2.0 (асинхронный) — ORM
- PostgreSQL — база данных
- Docker / Docker Compose — контейнеризация
- Pydantic v2 — валидация данных

## Запуск проекта

### Локальный запуск (без Docker)

1. Клонируйте репозиторий:
      git clone <url>
   cd fast_api_1
   

2. Создайте и активируйте виртуальное окружение:
      python -m venv .venv
   source .venv/bin/activate      # Linux/Mac
   .venv\Scripts\activate         # Windows
   

3. Установите зависимости:
      pip install -r requirements.txt
   

4. Создайте файл `.env` на основе .env.example и отредактируйте параметры подключения к PostgreSQL:
      POSTGRES_USER=my_user
   POSTGRES_PASSWORD=my_password
   POSTGRES_DB=my_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   

5. Убедитесь, что PostgreSQL запущен и база данных существует. При необходимости создайте пользователя и базу:
      CREATE USER my_user WITH PASSWORD 'my_password';
   CREATE DATABASE my_db OWNER my_user;
   

6. Запустите сервер:
      uvicorn app.app:app --reload
   

   Сервер будет доступен по адресу http://127.0.0.1:8000. Документация Swagger — http://127.0.0.1:8000/docs.

### Запуск через Docker

1. Убедитесь, что Docker и Docker Compose установлены.

2. Создайте файл `.env` на основе .env.example. Для Docker укажите POSTGRES_HOST=db (имя сервиса в compose):
      POSTGRES_USER=my_user
   POSTGRES_PASSWORD=my_password
   POSTGRES_DB=my_db
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   

3. Запустите контейнеры:
      docker-compose up --build
   

   Приложение будет доступно по адресу http://localhost:8080. Документация — http://localhost:8080/docs.

## Переменные окружения

| Переменная          | Описание                               | Пример значения    |
|---------------------|----------------------------------------|--------------------|
| POSTGRES_USER     | Имя пользователя PostgreSQL            | my_user          |
| POSTGRES_PASSWORD | Пароль пользователя                    | my_password      |
| POSTGRES_DB       | Название базы данных                   | my_db            |
| POSTGRES_HOST     | Хост PostgreSQL (локально: localhost, в Docker: db) | localhost |
| POSTGRES_PORT     | Порт PostgreSQL                        | 5432             |

## Примеры запросов

### Создание объявления
curl -X POST "http://localhost:8000/advertisement" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Продам велосипед",
    "description": "Спортивный, почти новый",
    "price": 15000.5,
    "author": "Иван Петров"
  }'

### Получение объявления по ID
curl "http://localhost:8000/advertisement/1"

### Обновление объявления
curl -X PATCH "http://localhost:8000/advertisement/1" \
  -H "Content-Type: application/json" \
  -d '{"price": 14000}'

### Удаление объявления
curl -X DELETE "http://localhost:8000/advertisement/1"

### Поиск объявлений
curl "http://localhost:8000/advertisement?title=велосипед&price_min=10000&price_max=20000"

## Структура проекта

fast_api_1/

├── app/

│   ├── __init__.py

│   ├── app.py              # основной файл FastAPI, эндпоинты

│   ├── config.py           # загрузка конфигурации из .env

│   ├── database.py         # настройка SQLAlchemy, engine, Base

│   ├── dependencies.py     # зависимости (get_db_session)

│   ├── lifespan.py         # создание таблиц при старте

│   ├── models.py           # SQLAlchemy модели

│   ├── schemas.py          # Pydantic схемы

│   └── services.py         # CRUD операции

├── .env.example             # пример переменных окружения

├── .gitignore

├── docker-compose.yml       # запуск приложения и PostgreSQL

├── Dockerfile

└── requirements.txt         # зависимости Python

## Примечания

- При первом запуске таблицы в базе данных создаются автоматически (через lifespan-менеджер).
- Для продакшена рекомендуется использовать систему миграций (например, Alembic).
- Авторизация и аутентификация не реализованы, так как не требовались в задании.
- Все эндпоинты возвращают данные в формате JSON.

### Скрин экрана примера проекта

![photo_2026-03-03_16-23-00](https://github.com/user-attachments/assets/b61dc1cf-20b5-456c-84a2-247120073300)
