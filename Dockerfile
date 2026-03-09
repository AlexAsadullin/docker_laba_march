# 1) Базовый образ с Python
FROM python:3.12-slim

# 2) Установка системных пакетов (LibreOffice для конвертации)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice && \
    rm -rf /var/lib/apt/lists/*

# 3) Создание рабочей папки и сборка проекта в ней
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /temp

EXPOSE 8000

# 4) При запуске контейнера автоматически стартует приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
