from pyrogram import Client
import time
import schedule
import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')

app = Client(name='my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def send_startup_message():
    """Фунция для проверки бота"""
    app.send_message('yantestc', "Бот запущен")


def send_good_morning():
    """Функция для отправки сообщения"""
    app.send_message('yantestc', "Доброе утро")


schedule.every().day.at("10:00").do(send_good_morning)  # Тут можно менять время отправки


def run_schedule():
    """Выполняется проверка задач с интервалом в секунду"""
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print("Error!", e)


if __name__ == "__main__":
    app.start()
    send_startup_message()
    run_schedule()
