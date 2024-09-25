from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema
from app.utils.custom_route import custom_route

bp = Blueprint('client_transaction', __name__)  # Name changed to client_transaction to avoid conflicts


# Client Routes
@custom_route(bp, '/list_my_transactions', methods=['GET'], schema=TransactionSchema, require_auth=True, allowed_roles="client")
def list_my_transactions(data):
    from app.logic.transaction.client.list_my_transactions import execute
    return execute(**data)


@custom_route(bp, '/transactions/<int:id>', methods=['GET'], schema=None, require_auth=True, allowed_roles="client")
def get_transaction_by_id(id):
    from app.logic.transaction.client.get_transaction_by_id import execute
    return execute(id)


@custom_route(bp, '/transactions/report', methods=['GET'], schema=None, require_auth=True, allowed_roles="client")
def get_my_transactions_report():
    from app.logic.transaction.client.get_my_transaction_report import execute
    return execute()


@custom_route(bp, '/create_transaction', methods=['POST'], schema=TransactionSchema, require_auth=True,
              allowed_roles="client")
def create_transaction(data):
    from app.logic.transaction.client.create_transaction import execute
    return execute(**data)
