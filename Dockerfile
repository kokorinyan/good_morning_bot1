FROM python:3.9-slim

# Установка необходимых инструментов и Microsoft ODBC Driver
RUN apt-get update && \
    apt-get install -y curl apt-transport-https gnupg unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --log /app/pip_log.txt

# Копирование исходного кода
COPY . .

# Копирование .env файла
COPY .env .

# Установка переменных окружения
ENV API_ID=$API_ID
ENV API_HASH=$API_HASH
ENV BOT_TOKEN=$BOT_TOKEN
ENV SUBSCRIPTION_KEY1=$SUBSCRIPTION_KEY1
ENV SUBSCRIPTION_KEY2=$SUBSCRIPTION_KEY2
ENV ENDPOINT=$ENDPOINT
ENV CUSTOM_CONFIG_ID=$CUSTOM_CONFIG_ID
ENV DB_CONNECTION_STRING=$DB_CONNECTION_STRING

# Команда для запуска приложения
CMD ["python", "main.py"]