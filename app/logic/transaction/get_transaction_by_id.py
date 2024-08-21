from app.models.transaction import Transaction
from app.utils.exceptions import appNotFoundError


def execute(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        raise appNotFoundError(f"Transaction with id {transaction_id} not found")

    return transaction.to_dict()
