# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем системные библиотеки для psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Сначала копируем зависимости (для кэширования слоев)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Делаем скрипт запуска исполняемым (опционально)
# Команда запуска: миграции + запуск сервера
CMD sh -c "alembic upgrade head && python3 main.py"