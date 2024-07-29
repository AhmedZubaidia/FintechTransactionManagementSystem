from app.third_parties.telegram.send_message import send_message


def send_new_user_notification(username):
    return send_message(f"Welcome {username}! You have successfully registered.")
