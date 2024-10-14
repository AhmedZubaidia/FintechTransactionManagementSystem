from flask import jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models.transaction_model import TransactionModel
from app.models.user_model import User
from app.third_parties.telegram.send_message import send_message
from app.utils.exceptions import appNotFoundError
from app.models.transaction_model import TransactionCategory, TransactionType


def execute(**data):
    amount = data.get('amount')
    category = data.get('category')
    transaction_type = data.get('transaction_type')
    description = data.get('description', None)
    user_id = data.get('user_id')
    user_id_token = data.get('user_id_token')

    # Ensure the user exists
    user = User.query.get(user_id)
    if not user or user.is_deleted:
        raise appNotFoundError(f"User with ID {user_id} not found or has been deleted")

    # Validate category and transaction type
    if not isinstance(category, TransactionCategory):
        raise ValueError("Invalid category")
    if not isinstance(transaction_type, TransactionType):
        raise ValueError("Invalid transaction type")

    new_transaction = TransactionModel(
        user_id=user_id,
        amount=amount,
        category=category.value,  # Use the enum value
        transaction_type=transaction_type.value,  # Use the enum value
        description=description
    )
    new_transaction.save(user_id_token)
    db.session.add(new_transaction)
    db.session.commit()

    return new_transaction
