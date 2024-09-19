from app.models.transaction_model import TransactionModel
from app.utils.exceptions import appNotFoundError


def execute(transaction_id):
    transaction = TransactionModel.query.get(transaction_id)
    if not transaction:
        raise appNotFoundError(f"Transaction with ID {transaction_id} not found")
    return transaction.to_dict()
