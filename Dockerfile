FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем alembic.ini и директорию alembic
COPY alembic.ini alembic.ini
COPY alembic alembic

# Копируем исходный код приложения
COPY app app

# Выполняем миграции и запускаем приложение
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
