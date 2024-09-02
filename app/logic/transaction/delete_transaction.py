from flask import jsonify, make_response
from app import db
from app.models.usertransaction import UserTransaction
from app.utils.exceptions import appNotFoundError


def execute(transaction_id):

    transaction = UserTransaction.query.get(transaction_id)
    if not transaction:
        raise appNotFoundError(f"Transaction with id {transaction_id} not found")

    db.session.delete(transaction)
    db.session.commit()

    return dict(
        message= "Transaction deleted successfully"
    )
