from app.third_parties.telegram.send_message import send_message


def send_login_notification(username):
    return send_message(f"{username} has logged in.")
