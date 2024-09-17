from app.models.transaction_model import TransactionModel


def execute():
    # Fetch all transactions
    transactions = TransactionModel.query.all()

    # Convert each transaction to a dictionary
    all_transactions = [transaction.to_dict() for transaction in transactions]

    # Return as a dictionary
    return {
        "transactions": all_transactions
    }
