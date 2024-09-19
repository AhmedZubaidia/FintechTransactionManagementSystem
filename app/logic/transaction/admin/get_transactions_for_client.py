from app.models.transaction_model import TransactionModel


def execute(client_id):
    transactions = TransactionModel.query.filter_by(user_id=client_id).all()
    if not transactions:
        return {"error": "No transactions found for this client"}, 404
    return [transaction.to_dict() for transaction in transactions], 200
