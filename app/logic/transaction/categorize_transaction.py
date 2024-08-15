from app import db
from app.models.transaction import Transaction
from app.utils.exceptions import NotFoundError


def execute(transaction_id, category):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        raise NotFoundError(f"Transaction with id {transaction_id} not found")

    transaction.category = category
    db.session.commit()
    return {'message': 'Transaction categorized successfully'}
