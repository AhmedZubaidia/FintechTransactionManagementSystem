from flask import jsonify, make_response
from app import db
from app.models.transaction import Transaction


def execute(user_id, amount, category, description=None, transaction_type=None):

    data = {
        'user_id': user_id,
        'amount': amount,
        'category': category,
        'description': description,
        'type': transaction_type
    }

    # Create the transaction object
    new_transaction = Transaction(**data)
    db.session.add(new_transaction)
    db.session.commit()

    return new_transaction
