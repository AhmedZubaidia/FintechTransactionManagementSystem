from flask_jwt_extended import get_jwt_identity
from app.models.transaction_model import TransactionModel


def execute():
    client_id = get_jwt_identity()  # Get the client ID from the JWT

    # Fetch all transactions for the client
    transactions = TransactionModel.query.filter_by(user_id=client_id).all()

    if not transactions:
        return {
            "user": {
                "id": client_id,
                "name": "Unknown"  # Adjust based on your user model
            },
            "credit": 0,
            "debit": 0,
            "balance": 0,
            "last_transaction_datetime": None
        }

    # Initialize credit, debit, and balance
    credit = 0
    debit = 0

    # Loop through transactions to calculate credit and debit
    for tx in transactions:
        if tx.transaction_type.value == 'credit':
            credit += tx.amount
        elif tx.transaction_type.value == 'debit':
            debit += tx.amount

    balance = credit - debit

    # Get the last transaction datetime
    last_transaction = max(transactions, key=lambda tx: tx.timestamp)

    # Prepare the final report
    report = {
        "user": {
            "id": client_id,
            "name": "client"  # Adjust based on your user model
        },
        "credit": credit,
        "debit": debit,
        "balance": balance,
        "last_transaction_datetime": last_transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

    return report
