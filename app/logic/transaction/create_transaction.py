from flask import jsonify, make_response
from app import db
from app.models.usertransaction import UserTransaction


def execute(user_id, amount, category, description=None, transaction_type=None):
    data = {
        'user_id': user_id,
        'amount': amount,
        'category': category,
        'description': description,
        'type': transaction_type
    }

    new_transaction = UserTransaction(**data)
    db.session.add(new_transaction)
    db.session.commit()

    new_transaction.created_by = user_id
    new_transaction.modified_by = user_id

    db.session.commit()

    return new_transaction
