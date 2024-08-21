from flask import Blueprint

from app.schemas.user_schema import UserSchema
from app.utils.custom_route import custom_route

bp = Blueprint('profile', __name__)


@custom_route(bp, '/users', methods=['GET'], schema=UserSchema, require_auth=True)
def get_users(data):
    from app.logic.auth.get_clients import execute
    return execute()


@custom_route(bp, '/users/<int:id>', methods=['DELETE'], require_auth=True)
def delete_user_route(data):
    from app.logic.auth.delete_client import execute
    return execute(data['id'])


@custom_route(bp, '/users/<int:id>', methods=['PUT'],schema=UserSchema, require_auth=True)
def update_user_route(data):
    from app.logic.auth.update_user import execute
    return execute(data['id'], **data)
