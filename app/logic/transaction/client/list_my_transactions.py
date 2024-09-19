from flask_jwt_extended import get_jwt_identity
from app.models.transaction_model import TransactionModel

from flask_jwt_extended import get_jwt_identity
from app.models.transaction_model import TransactionModel


def execute(page, per_page):
    client_id = get_jwt_identity()  # Get the client ID from the JWT

    # Query transactions for the client
    transactions_query = TransactionModel.query.filter_by(user_id=client_id)

    # Use pagination correctly (only pass page and per_page)
    paginated_transactions = transactions_query.paginate(page=page, per_page=per_page, error_out=False)

    # Get the list of items and total count
    transactions = [transaction.to_dict() for transaction in paginated_transactions.items]
    total_items = paginated_transactions.total

    return transactions, total_items
