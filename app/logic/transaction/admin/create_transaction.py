from app.models.transaction_model import TransactionModel
from app.models.user_model import User
from app.schemas.transaction_schema import TransactionSchema
from app.utils.exceptions import appNotFoundError


def execute(data):
    user_id = data.get("user_id")
    amount = data.get("amount")
    category = data.get("category")
    type = data.get("type")
    description = data.get("description")

    # Ensure the user exists
    user = User.query.get(user_id)
    if not user:
        raise appNotFoundError(f"User with ID {user_id} not found")

    # Create the transaction
    new_transaction = TransactionModel(
        user_id=user_id,
        amount=amount,
        category=category,
        type=type,
        description=description
    )
    new_transaction.save()
    return new_transaction.to_dict(), 201
