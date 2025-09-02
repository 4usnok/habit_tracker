import requests
from django.conf import settings


def send_tg_message(chat_id, message):

    params = {"text": message, "chat_id": chat_id}
    url = f"https://api.telegram.org/bot/{settings.BOT_TOKEN}/sendMessage"
    requests.post(url, params=params)
