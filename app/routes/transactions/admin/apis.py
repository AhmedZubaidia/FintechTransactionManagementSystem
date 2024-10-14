from flask import Blueprint
from app.schemas.transaction_schema import TransactionSchema, reportSchema, TransactionOutputSchema
from app.utils.custom_route import custom_route

bp = Blueprint('admin_transaction', __name__)


# Admin Routes
@custom_route(bp, '/create_transaction_admin/<int:user_id>', methods=['POST'], schema=TransactionSchema,
              require_auth=True, allowed_roles="admin", append_token_key=['user_id'])
def create_transaction_admin(data):
    from app.logic.transaction.admin.create_transaction import execute
    return execute(**data)


@custom_route(bp, '/transactions', methods=['GET'], schema=TransactionSchema, require_auth=True, allowed_roles="admin",
              paginate=True)
def get_all_transactions_admin(data):
    from app.logic.transaction.admin.get_all_transactions import execute
    return execute(**data)


@custom_route(bp, '/transactions/client/<int:user_id>', methods=['GET'], schema=TransactionSchema, require_auth=True,
              allowed_roles="admin", paginate=True)
def get_transactions_for_client_admin(data):
    from app.logic.transaction.admin.get_transactions_for_client import execute
    return execute(**data)


@custom_route(bp, '/transactions_report/client/<int:user_id>', methods=['GET'], schema=reportSchema, require_auth=True,
              allowed_roles="admin")
def generate_transaction_report_admin(data):
    from app.logic.transaction.admin.generate_transaction_report import execute
    return execute(**data)


@custom_route(bp, '/transactions/<int:id>', methods=['GET'], schema=None, require_auth=True,
              allowed_roles="admin")
def get_transaction_admin(id):
    from app.logic.transaction.admin.get_transaction_by_id import execute
    return execute(id)


@custom_route(bp, '/delete_transaction/<int:id>', methods=['DELETE'], schema=TransactionOutputSchema, require_auth=True,
              allowed_roles="admin", append_token_key=['user_id'])
def delete_transaction(data):
    from app.logic.transaction.admin.delete_transaction import execute
    return execute(**data)

