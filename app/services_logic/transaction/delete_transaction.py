from app import db
from app.models.transaction import Transaction

def execute(transaction):
    db.session.delete(transaction)
    db.session.commit()
    return {'message': 'Transaction deleted successfully'}, 200
