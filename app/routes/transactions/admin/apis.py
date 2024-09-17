from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema
from app.utils.custom_route import custom_route

bp = Blueprint('admin_transaction', __name__)


# Admin Routes
@custom_route(bp, '/create_transaction_admin/<int:user_id>', methods=['POST'], schema=TransactionSchema,
              require_auth=True, allowed_roles="admin")
def create_transaction_admin(user_id, data):
    from app.logic.transaction.admin.create_transaction import execute
    return execute(user_id, data)


@custom_route(bp, '/transactions', methods=['GET'], schema=None, require_auth=True, allowed_roles="admin")
def get_all_transactions_admin():
    from app.logic.transaction.admin.get_all_transactions import execute
    return execute()


@custom_route(bp, '/transactions/client/<int:client_id>', methods=['GET'], schema=None, require_auth=True,
              allowed_roles="admin")
def get_transactions_for_client_admin(client_id):
    from app.logic.transaction.admin.get_transactions_for_client import execute
    return execute(client_id)


@custom_route(bp, '/transactions_report/client/<int:client_id>', methods=['GET'], require_auth=True,
              allowed_roles="admin")
def generate_transaction_report_admin(client_id):
    from app.logic.transaction.admin.generate_transaction_report import execute
    return execute(client_id)


@custom_route(bp, '/transactions/<int:id>', methods=['GET'], schema=None, require_auth=True,
              allowed_roles="admin")
def get_transaction_admin(id):
    from app.logic.transaction.admin.get_transaction_by_id import execute
    return execute(id)


@custom_route(bp, '/transactions/<int:transaction_id>', methods=['DELETE'], schema=TransactionSchema, require_auth=True,
              allowed_roles="admin")
def delete_transaction_admin(transaction_id):
    from app.logic.transaction.admin.delete_transaction import execute
    return execute(transaction_id)
