from app.third_parties.telegram.send_message import send_message


def send_user_deletion_notification(username):
    return send_message(f"{username} has been deleted.")
