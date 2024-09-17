from flask_jwt_extended import get_jwt_identity
from app.models.transaction_model import TransactionModel


def execute():
    client_id = get_jwt_identity()  # Get the client ID from the JWT

    # Fetch all transactions for the client
    transactions = TransactionModel.query.filter_by(user_id=client_id).all()

    # Create a list of transactions using the `to_dict()` method for each transaction
    transactions_report = [transaction.to_dict() for transaction in transactions]

    # Prepare the final report
    report = {
        "user": {
            "id": client_id,
        },
        "transactions": transactions_report,  # Include all transactions
        "total_transactions": len(transactions_report)  # Optionally, include the total count
    }

    return report
