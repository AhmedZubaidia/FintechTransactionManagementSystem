from pickle import GET

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required
from app.logic.auth import login_client, register_client, get_clients, delete_client
from app.utils.custom_route import custom_route

bp = Blueprint('profile', __name__)


@custom_route(bp, '/users', methods=['GET'], require_auth=True)
def get_users(data):
    return get_clients.execute()


@custom_route(bp, '/users/<int:id>', methods=['DELETE'], require_auth=True)
def delete_user_route(data):
    return delete_client.execute(data['id'])
