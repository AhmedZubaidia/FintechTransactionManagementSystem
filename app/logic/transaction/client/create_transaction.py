from flask import jsonify, make_response, current_app
from flask_jwt_extended import get_jwt_identity

from app import db
from app.models.transaction_model import TransactionModel
from app.models.user_model import User
from app.third_parties.telegram.send_message import send_message
from app.utils.exceptions import appNotFoundError

from app.models.transaction_model import TransactionCategory, TransactionType


def execute(amount, category, description=None, transaction_type=None , user_id_token=None):

    # Ensure the user exists
    user = User.query.get(user_id_token)
    if not user:
        raise appNotFoundError(f"User with ID {user_id_token} not found")

    # Validate category and transaction type
    if not isinstance(category, TransactionCategory):
        raise ValueError("Invalid category")
    if not isinstance(transaction_type, TransactionType):
        raise ValueError("Invalid transaction type")

    # Create the transaction
    new_transaction = TransactionModel(
        user_id=user_id_token,
        amount=amount,
        category=category.value,  # Use the enum value
        transaction_type=transaction_type.value,  # Use the enum value
        description=description
    )
    new_transaction.save(user_id_token, is_new=True)

    chat_id = current_app.config['TELEGRAM_CHAT_ID']
    message = f"New transaction recorded for user {user.username} with amount {amount}"
    send_message(message, chat_id)

    return new_transaction.to_dict()