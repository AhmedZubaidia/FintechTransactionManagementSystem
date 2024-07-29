from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services_logic.transaction import create_transaction, get_transactions, update_transaction, delete_transaction

bp = Blueprint('transaction', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_transactions_route():
    response, status_code = get_transactions.execute()
    return make_response(jsonify(response), status_code)


@bp.route('', methods=['POST'])
@jwt_required()
def create_transaction_route():
    data = request.get_json()
    user_id = get_jwt_identity()
    response, status_code = create_transaction.execute(user_id, **data)
    return make_response(jsonify(response), status_code)


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_transaction(id):
    response, status_code = get_transactions.execute_by_id(id)
    return make_response(jsonify(response), status_code)


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_transaction_route(id):
    data = request.get_json()
    transaction_response, transaction_status_code = get_transactions.execute_by_id(id)
    if transaction_status_code != 200:
        return make_response(jsonify(transaction_response), transaction_status_code)
    transaction = transaction_response
    response, status_code = update_transaction.execute(transaction, **data)
    return make_response(jsonify(response), status_code)


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction_route(id):
    transaction_response, transaction_status_code = get_transactions.execute_by_id(id)
    if transaction_status_code != 200:
        return make_response(jsonify(transaction_response), transaction_status_code)
    transaction = transaction_response
    response, status_code = delete_transaction.execute(transaction)
    return make_response(jsonify(response), status_code)
