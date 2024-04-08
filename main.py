from pyrogram import Client
import time
import schedule

api_id = 24639906
api_hash = 'a125d1dd3a48acafb671a4033c8e2ce5'
bot_token = '6946754420:AAGVbbxuvU-HZA1ehjfdBl01LdOSOfcV_Ow'

app = Client(name='my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def send_good_morning():
    """Функция для отправки сообщения"""
    app.send_message('yantestc', "Доброе утро")


schedule.every().day.at("12:23").do(send_good_morning)  # Тут можно менять время отправки


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
    run_schedule()
