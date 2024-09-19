from flask_jwt_extended import get_jwt_identity
from app.models.transaction_model import TransactionModel


def execute():
    client_id = get_jwt_identity()  # Get the client ID from the JWT
    transactions = TransactionModel.query.filter_by(user_id=client_id).all()
    return [transaction.to_dict() for transaction in transactions], 200
