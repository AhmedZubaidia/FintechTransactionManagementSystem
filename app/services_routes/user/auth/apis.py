from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required
from app.services_logic.auth import login_client, register_client, get_clients, delete_client

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = register_client.execute(**data)
    return make_response(jsonify(response), status_code)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user, status_code = login_client.execute(**data)
    if status_code != 200:
        return make_response(jsonify(user), status_code)
    access_token = create_access_token(identity=user.id)
    return make_response(jsonify({'message': 'Login successful', 'access_token': access_token}), 200)

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users, status_code = get_clients.execute()
    return make_response(jsonify(users), status_code)

@bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(id):
    user = get_clients.get_user_by_id(id)
    if not user:
        return make_response(jsonify({'message': 'User not found'}), 404)
    response, status_code = delete_client.execute(user)
    return make_response(jsonify(response), status_code)

