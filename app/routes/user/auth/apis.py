from flask import Blueprint
from app.schemas.user_schema import LoginSchema, RegisterSchema
from app.utils.custom_route import custom_route

bp = Blueprint('auth', __name__)


@custom_route(bp, '/v1/register', methods=['POST'], schema=RegisterSchema, require_auth=False)
def register(data):
    from app.logic.auth.register_client import execute
    return execute(**data)


@custom_route(bp, '/v1/login', methods=['POST'], schema=LoginSchema, require_auth=False)
def login(data):
    from app.logic.auth.login_client import execute
    return execute(**data)
