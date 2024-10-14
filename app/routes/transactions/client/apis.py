from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema, TransactionClientSchema, TransactionOutputSchema, \
    reportSchema
from app.utils.custom_route import custom_route

bp = Blueprint('client_transaction', __name__)  # Name changed to client_transaction to avoid conflicts


# Client Routes
@custom_route(bp, '/list_my_transactions', methods=['GET'], schema=TransactionClientSchema, require_auth=True,
              allowed_roles="client", paginate=True, append_token_key=['user_id'])
def list_my_transactions(data):
    from app.logic.transaction.client.list_my_transactions import execute
    return execute(**data)


@custom_route(bp, '/transactions/<int:id>', methods=['GET'], schema=TransactionOutputSchema, require_auth=True, allowed_roles="client" , append_token_key=['user_id'])
def get_transaction_by_id(data):
    from app.logic.transaction.client.get_transaction_by_id import execute
    return execute(**data)


@custom_route(bp, '/transactions/report', methods=['GET'], schema=reportSchema, require_auth=True, allowed_roles="client",
              append_token_key=['user_id'])
def get_my_transactions_report(data):
    from app.logic.transaction.client.get_my_transaction_report import execute
    return execute(**data)


@custom_route(bp, '/create_transaction', methods=['POST'], schema=TransactionClientSchema, require_auth=True,
              allowed_roles="client", append_token_key=['user_id'])
def create_transaction(data):
    from app.logic.transaction.client.create_transaction import execute
    return execute(**data)


