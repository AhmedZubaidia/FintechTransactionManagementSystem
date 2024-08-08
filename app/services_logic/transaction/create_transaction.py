from app.models.transaction import Transaction
from app import db
from app.third_parties.telegram.send_transaction_notification import send_transaction_notification

def execute(user_id, amount, category, description):
    new_transaction = Transaction(user_id=user_id, amount=amount, category=category, description=description)
    db.session.add(new_transaction)
    db.session.commit()

    send_transaction_notification(amount, category)

    return {'message': 'Transaction created successfully'}, 201
