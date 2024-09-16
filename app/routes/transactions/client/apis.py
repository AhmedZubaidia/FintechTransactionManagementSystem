from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema
from app.utils.custom_route import custom_route

bp = Blueprint('transaction', __name__)


# Client Route to list their own transactions with pagination
@custom_route(bp, '/client/transactions', methods=['GET'], schema=TransactionSchema, require_auth=True,
              allowed_roles="client")
def list_my_transactions():
    from app.logic.transaction.client.list_my_transactions import execute
    return execute()


# Client Route to get a specific transaction by ID
@custom_route(bp, '/client/transactions/<int:id>', methods=['GET'], schema=TransactionSchema, require_auth=True,
              allowed_roles="client")
def get_transaction_by_id(id):
    from app.logic.transaction.client.get_transaction_by_id import execute
    return execute(id)


# Client Route to get their transaction report
@custom_route(bp, '/client/transactions/report', methods=['GET'], require_auth=True, allowed_roles="client")
def get_my_transaction_report():
    from app.logic.transaction.client.get_my_transaction_report import execute
    return execute()


@custom_route(bp, '/client/create_transaction', methods=['POST'], schema=TransactionSchema, require_auth=True,
              allowed_roles="client")
def create_transaction(data):
    from app.logic.transaction.client.create_transaction import execute
    return execute(**data)
