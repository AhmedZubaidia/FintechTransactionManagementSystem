from flask import make_response, jsonify

from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionSchema


def execute():

    transactions = Transaction.query.all()
    transactions_list = [
        {'id': t.id, 'user_id': t.user_id, 'amount': t.amount, 'category': t.category, 'description': t.description,
         'timestamp': t.timestamp} for t in transactions]
    return transactions_list, 200
