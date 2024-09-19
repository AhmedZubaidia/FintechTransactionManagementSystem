from app.models.transaction_model import TransactionModel


def execute():
    transactions = TransactionModel.query.all()
    return [transaction.to_dict() for transaction in transactions], 200
