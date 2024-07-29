from app.third_parties.telegram.send_message import send_message


def send_error_notification(message):
    return send_message(f"Error: {message}")
