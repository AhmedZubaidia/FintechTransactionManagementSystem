# app/logic/transaction/client/delete_transaction.py
from app.models.transaction_model import TransactionModel
from app import db


def execute(id, user_id_token):
    transaction = TransactionModel.query.get(id)

    # Check if the transaction exists, belongs to the current user, and is not already deleted
    if not transaction or transaction.is_deleted:
        return {"error": "Transaction not found or be deleted or not belong to the current user"}

    # Perform soft delete
    transaction.save(user_id_token)
    transaction.soft_delete()
    db.session.commit()

    return {"message": "Transaction soft deleted successfully"}
