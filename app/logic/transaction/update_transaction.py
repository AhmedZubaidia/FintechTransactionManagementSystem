from app import db
from app.models.transaction import Transaction
from app.utils.exceptions import NotFoundError


def execute(transaction_id, amount=None, category=None, description=None, transaction_type=None):

    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        raise NotFoundError(f"Transaction with id {transaction_id} not found")

    # Create a dictionary for the incoming data
    data = {
        'amount': amount,
        'category': category,
        'description': description,
        'type': transaction_type
    }

    # Filter out None values to avoid overwriting existing fields with None
    data = {key: value for key, value in data if value is not None}

    # Update the transaction object
    for key, value in data.items():
        setattr(transaction, key, value)

    db.session.commit()

    return {'message': 'Transaction updated successfully'}



