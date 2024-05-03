import requests
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


def get_bing_news(search_term):
    """Функция принимает и отправляет bing новости в канал"""
    subscription_key1 = os.environ.get('SUBSCRIPTION_KEY1')
    subscription_key2 = os.environ.get('SUBSCRIPTION_KEY2')

    endpoint = os.environ.get('ENDPOINT')
    custom_config_id = os.environ.get('CUSTOM_CONFIG_ID')
    market = "en-US"

    url = (endpoint + "v7.0/custom/search?q=" + search_term + "&customconfig=" +
           custom_config_id + "&mkt=" + market)

    headers1 = {'Ocp-Apim-Subscription-Key': subscription_key1}
    headers2 = {'Ocp-Apim-Subscription-Key': subscription_key2}

    response1 = requests.get(url, headers=headers1)

    if response1.status_code == 401:
        response2 = requests.get(url, headers=headers2)
        data = response2.json()
    else:
        data = response1.json()

    if 'webPages' in data:
        news = data['webPages']['value']
        for article in news:
            try:
                app.send_message('yantestc', f"{article['name']}: {article['url']}")
            except Exception as e:
                print("Error", e)
        return news
    else:
        app.send_message('yantestc', "Новости не найдены")


def send_good_morning():
    """Функция для отправки сообщения"""
    app.send_message('yantestc', "Доброе утро")


def run_schedule():
    """Выполняется проверка задач с интервалом в секунду"""
    try:
        while True:
            schedule.every().day.at("10:00").do(send_good_morning)  # Тут можно менять время отправки
            schedule.every().day.at("10:00").do(lambda: get_bing_news('technology'))
            schedule.every().day.at("12:00").do(lambda: get_bing_news('technology'))
            schedule.every().day.at("14:30").do(lambda: get_bing_news('technology'))
            schedule.every().day.at("17:00").do(lambda: get_bing_news('technology'))
            while True:
                schedule.run_pending()
                time.sleep(1)
    except Exception as e:
        print("Error!", e)


if __name__ == "__main__":
    app.start()
    send_startup_message()
    get_bing_news('technology')
    run_schedule()
