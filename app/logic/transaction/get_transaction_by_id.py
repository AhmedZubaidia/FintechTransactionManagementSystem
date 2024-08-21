from app.models.transaction import Transaction
from app.utils.exceptions import NotFoundError


def execute(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        raise NotFoundError(f"Transaction with id {transaction_id} not found")

    return transaction.to_dict()
