FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .

ENV API_ID=$API_ID
ENV API_HASH=$API_HASH
ENV BOT_TOKEN=$BOT_TOKEN

CMD ["python", "main.py"]
