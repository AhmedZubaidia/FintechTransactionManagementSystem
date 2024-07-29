import requests
from flask import current_app


def send_message(message):
    token = current_app.config['TELEGRAM_TOKEN']
    chat_id = current_app.config['TELEGRAM_CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()
