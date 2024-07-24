import requests

def send_telegram_message(chat_id, text):
    token = '7270283184:AAHZuYyjsT33FY8oBqM0ccRbT5-mYTzLb7Q'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()
