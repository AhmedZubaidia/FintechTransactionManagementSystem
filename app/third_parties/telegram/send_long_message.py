from app.third_parties.telegram.send_message import send_message


def send_long_message(message, chat_id):
    # Telegram's maximum message length is 4096 characters
    max_message_length = 4096

    # Split the message into chunks of 4096 characters
    for i in range(0, len(message), max_message_length):
        chunk = message[i:i + max_message_length]
        response = send_message(chunk, chat_id)

        # Optional: Check the response to see if there were errors
        if not response.get("ok"):
            print(f"Failed to send message chunk: {response}")
