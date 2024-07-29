from app.third_parties.telegram.send_message import send_message


def send_transaction_notification(amount, category):
    return send_message(f"Transaction created: {amount} in {category} category.")
