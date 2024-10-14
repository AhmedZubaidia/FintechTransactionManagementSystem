from app.models.transaction_model import TransactionModel
from app.utils.exceptions import appNotFoundError


def execute(user_id, page, per_page):
    transactions = TransactionModel.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)

    # Check if there are transactions for the user
    if transactions.total == 0:
        raise appNotFoundError(f"User with ID {user_id} has no transactions")

    # Return the pagination object directly
    return transactions
