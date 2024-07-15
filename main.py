import requests
from pyrogram import Client
import time
import schedule
import pyodbc
from environs import Env

env = Env()
env.read_env('./.env')
api_id = env.int('API_ID')
api_hash = env.str('API_HASH')
bot_token = env.str('BOT_TOKEN')
db_connection_string = env.str('DB_CONNECTION_STRING')


app = Client(name='my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def get_db_connection():
    conn = pyodbc.connect(db_connection_string)
    return conn


def news_exist(title, url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM SentNews WHERE Title = ? AND Url = ?", (title, url))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists


def save_news(title, url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SentNews (Title, Url) VALUES (?, ?)", (title, url))
    conn.commit()
    conn.close()


def get_bing_news(search_term):
    """Функция принимает и отправляет bing новости в канал"""
    subscription_key1 = env.str('SUBSCRIPTION_KEY1')
    subscription_key2 = env.str('SUBSCRIPTION_KEY2')

    endpoint = env.str('ENDPOINT')
    custom_config_id = env.str('CUSTOM_CONFIG_ID')
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

    new_news_found = False

    if 'webPages' in data:
        news = data['webPages']['value']
        for article in news:
            title = article['name']
            url = article['url']
            if not news_exist(title, url):
                try:
                    app.send_message('yantestc', f"{article['name']}: {article['url']}")
                    save_news(title, url)
                    new_news_found = True
                except Exception as e:
                    print("Error", e)
        if not new_news_found:
            app.send_message('yantestc', "Новых новостей пока нет")
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
            schedule.every().day.at("14:00").do(lambda: get_bing_news('technology'))
            schedule.every().day.at("17:00").do(lambda: get_bing_news('technology'))
            while True:
                schedule.run_pending()
                time.sleep(1)
    except Exception as e:
        print("Error!", e)


# test functions
def send_startup_message():
    """Фунция для проверки бота"""
    app.send_message('yantestc', "Бот запущен")


def test_db_connection():
    try:
        conn = pyodbc.connect(db_connection_string)
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")


def print_saved_news():
    """Функция для получения и вывода сохраненной информации из базы данных в консоль"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Title, Url FROM SentNews")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Title: {row[0]}, URL: {row[1]}")
    conn.close()


def test_code():
    send_startup_message()
    test_db_connection()
    print_saved_news()


if __name__ == "__main__":
    app.start()
    test_code()
    get_bing_news('technology')
    run_schedule()
