# app/logic/transaction/admin/delete_transaction.py
from app.models.transaction_model import TransactionModel
from app import db


def execute(transaction_id):
    transaction = TransactionModel.query.get(transaction_id)
    if not transaction:
        return {"error": "Transaction not found"}, 404

    db.session.delete(transaction)
    db.session.commit()
    return {"message": "Transaction deleted successfully"}