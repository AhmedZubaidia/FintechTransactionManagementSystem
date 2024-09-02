from app import db
from app.models.usertransaction import UserTransaction
from app.utils.exceptions import appNotFoundError


def execute(transaction_id, category):
    transaction = UserTransaction.query.get(transaction_id)
    if transaction is None:
        raise appNotFoundError(f"Transaction with id {transaction_id} not found")

    transaction.category = category
    db.session.commit()
    return {'message': 'Transaction categorized successfully'}
