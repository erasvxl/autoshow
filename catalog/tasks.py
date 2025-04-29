from celery import shared_task
import requests

@shared_task
def send_telegram_message(message):
    bot_token = 'your_bot_token'
    chat_id = 'your_chat_id'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': message})
from celery import shared_task
import requests
from django.conf import settings

@shared_task
def send_telegram_message(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': message})
from celery import shared_task
import requests
from django.conf import settings

@shared_task
def send_telegram_message(message):
    # Логируем входящую задачу
    print(">> [TASK] собираемся отправить в Telegram:", message)
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        'chat_id': settings.TELEGRAM_CHAT_ID,
        'text': message,
    })
    # Логируем ответ от Telegram API
    print("<< [TASK] ответ Telegram:", resp.status_code, resp.text)
