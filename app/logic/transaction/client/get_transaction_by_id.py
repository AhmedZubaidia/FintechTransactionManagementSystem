from flask_jwt_extended import get_jwt_identity

from app.models.transaction_model import TransactionModel
from app.utils.exceptions import appNotFoundError, appForbiddenError


def execute(id, user_id_token=None):
    transaction = TransactionModel.query.get(id)

    if not transaction:
        raise appNotFoundError(f"Transaction with ID {id} not found")

    # Check if the transaction belongs to the current user
    if transaction.user_id != user_id_token:
        raise appForbiddenError("No Transaction with ID {transaction_id} found for the current user")

    return transaction.to_dict()
