from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models.transaction_model import TransactionModel
from app.models.user_model import User
from app.utils.exceptions import appNotFoundError
from app.models.transaction_model import TransactionCategory, TransactionType


def execute(user_id, data):
    amount = data.get('amount')
    category = data.get('category')
    transaction_type = data.get('transaction_type')
    description = data.get('description', None)

    # Ensure the user exists
    user = User.query.get(user_id)
    if not user:
        raise appNotFoundError(f"User with ID {user_id} not found")

    # Convert category and transaction_type to their enum types
    try:
        category_enum = TransactionCategory[category.upper()]  # Convert string to enum
        transaction_type_enum = TransactionType[transaction_type.upper()]  # Convert string to enum
    except KeyError:
        raise appNotFoundError("Invalid category or transaction type")

    # Create the transaction
    new_transaction = TransactionModel(
        user_id=user_id,
        amount=amount,
        category=category_enum.value,  # Use the enum value
        transaction_type=transaction_type_enum.value,  # Use the enum value
        description=description
    )
    db.session.add(new_transaction)
    db.session.commit()

    return new_transaction.to_dict()
