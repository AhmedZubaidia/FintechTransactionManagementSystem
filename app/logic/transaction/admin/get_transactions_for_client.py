from app.models.transaction_model import TransactionModel
from app.utils.exceptions import appNotFoundError


def execute(client_id):
    transactions = TransactionModel.query.filter_by(user_id=client_id).all()
    if not transactions:
        raise appNotFoundError(f"User with ID {client_id} has no transactions")

    all_transactions_for_user = [transaction.to_dict() for transaction in transactions]
    return {
        "transactions": all_transactions_for_user
    }
