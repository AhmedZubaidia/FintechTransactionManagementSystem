from app.models.transaction import Transaction
from app import db

def execute(transaction, amount, category, description):
    transaction.amount = amount
    transaction.category = category
    transaction.description = description
    db.session.commit()
    return {'message': 'Transaction updated successfully'}, 200
