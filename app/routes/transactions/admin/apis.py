# Admin Route to create a transaction for a client
from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema
from app.utils.custom_route import custom_route

bp = Blueprint('transaction', __name__)


@custom_route(bp, '/admin/transactions', methods=['POST'], schema=TransactionSchema, require_auth=True,
              allowed_roles="admin")
def create_transaction_admin():
    from app.logic.transaction.admin.create_transaction import execute
    return execute()


# Admin Route to list all transactions with pagination
@custom_route(bp, '/admin/transactions', methods=['GET'], schema=TransactionSchema, require_auth=True,
              allowed_roles="admin")
def get_all_transactions_admin():
    from app.logic.transaction.admin.get_all_transactions import execute
    return execute()


# Admin Route to get transactions for a specific client
@custom_route(bp, '/admin/transactions/client/<int:client_id>', methods=['GET'], schema=TransactionSchema,
              require_auth=True,
              allowed_roles="admin")
def get_transactions_for_client_admin(client_id):
    from app.logic.transaction.admin.get_transactions_for_client import execute
    return execute(client_id)


# Admin Route to generate a report for a specific client
@custom_route(bp, '/admin/transactions/client/<int:client_id>/report', methods=['GET'], require_auth=True,
              allowed_roles="admin")
def generate_transaction_report_admin(client_id):
    from app.logic.transaction.admin.generate_transaction_report import execute
    return execute(client_id)


# Admin Route to get a specific transaction by ID
@custom_route(bp, '/admin/transactions/<int:id>', methods=['GET'], schema=TransactionSchema, require_auth=True,
              allowed_roles="admin")
def get_transaction_admin(id):
    from app.logic.transaction.admin.get_transactions_for_client import execute
    return execute(id)


# Admin Route to delete a transaction by ID
@custom_route(bp, '/admin/transactions/<int:transaction_id>', methods=['DELETE'], schema=TransactionSchema,
              require_auth=True, allowed_roles="admin")
def delete_transaction_admin(transaction_id):
    from app.logic.transaction.admin.delete_transaction import execute
    return execute(transaction_id)
