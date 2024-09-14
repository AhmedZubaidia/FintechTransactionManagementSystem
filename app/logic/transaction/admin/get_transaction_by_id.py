from app.models.transaction_model import TransactionModel


def execute(transaction_id):
    transaction = TransactionModel.query.get(transaction_id)
    if not transaction:
        return {"error": "Transaction not found"}, 404
    return transaction.to_dict(), 200
