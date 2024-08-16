
from app.third_parties.telegram.send_message import send_message


def send_long_message(message, chat_id):
    # Split the message into chunks of 4096 characters
    for i in range(0, len(message), 4096):
        send_message(message[i:i + 4096], chat_id)

