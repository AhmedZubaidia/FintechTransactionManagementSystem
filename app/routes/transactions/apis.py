from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema
from app.utils.custom_route import custom_route

bp = Blueprint('transaction', __name__)


@custom_route(bp, '', methods=['GET'], schema=TransactionSchema, require_auth=True)
def get_transactions_route():
    from app.logic.transaction.get_transactions import execute
    return execute()


@custom_route(bp, '/transactions', methods=['POST'], schema=TransactionSchema, require_auth=True)
def create_transaction_route(data):
    from app.logic.transaction.create_transaction import execute
    return execute(**data)


@custom_route(bp, '/<int:id>', methods=['GET'], schema=TransactionSchema, require_auth=True)
def get_transaction(id):
    from app.logic.transaction.get_transaction_by_id import execute
    return execute(id)


@custom_route(bp, '/<int:transaction_id>', methods=['PUT'], schema=TransactionSchema, require_auth=True)
def update_transaction_route(transaction_id, data):
    from app.logic.transaction.update_transaction import execute
    return execute(transaction_id, **data)


@custom_route(bp, '/<int:transaction_id>', methods=['DELETE'], schema=TransactionSchema, require_auth=True)
def delete_transaction_route(transaction_id):
    from app.logic.transaction.delete_transaction import execute
    return execute(transaction_id)
