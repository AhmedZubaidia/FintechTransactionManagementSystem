from flask import jsonify, make_response
from app import db
from app.models.transaction import Transaction
from app.utils.exceptions import NotFoundError


def execute(transaction_id):

    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        raise NotFoundError(f"Transaction with id {transaction_id} not found")

    db.session.delete(transaction)
    db.session.commit()

    return dict(
        message= "Transaction deleted successfully"
    )
