from flask import request, jsonify, make_response
from FintechTransactionManagementSystem.models import User, Transaction
from FintechTransactionManagementSystem.app import db
from werkzeug.security import generate_password_hash, check_password_hash

def register_routes(app, db):
    @app.route('/')
    def index():
        return make_response(jsonify({"message": "Welcome to the API!"}), 200)

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in users]
        return make_response(jsonify(users_list), 200)

    @app.route('/transactions', methods=['GET'])
    def get_transactions():
        transactions = Transaction.query.all()
        transactions_list = [{
            'id': transaction.id,
            'user_id': transaction.user_id,
            'amount': transaction.amount,
            'category': transaction.category,
            'description': transaction.description,
            'timestamp': transaction.timestamp
        } for transaction in transactions]
        return make_response(jsonify(transactions_list), 200)

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return make_response(jsonify({'message': 'User already exists'}), 400)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({'message': 'User registered successfully'}), 201)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return make_response(jsonify({'message': 'Login failed'}), 401)

        return make_response(jsonify({'message': 'Login successful'}), 200)

    @app.route('/transactions', methods=['POST'])
    def create_transaction():
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        category = data.get('category')
        description = data.get('description')

        new_transaction = Transaction(user_id=user_id, amount=amount, category=category, description=description)
        db.session.add(new_transaction)
        db.session.commit()

        return make_response(jsonify({'message': 'Transaction created successfully'}), 201)

    @app.route('/transactions/<int:id>', methods=['GET'])
    def get_transaction(id):
        transaction = Transaction.query.get(id)
        if not transaction:
            return make_response(jsonify({'message': 'Transaction not found'}), 404)

        return make_response(jsonify({
            'id': transaction.id,
            'user_id': transaction.user_id,
            'amount': transaction.amount,
            'category': transaction.category,
            'description': transaction.description,
            'timestamp': transaction.timestamp
        }), 200)

    @app.route('/transactions/<int:id>', methods=['PUT'])
    def update_transaction(id):
        data = request.get_json()
        transaction = Transaction.query.get(id)

        if not transaction:
            return make_response(jsonify({'message': 'Transaction not found'}), 404)

        transaction.amount = data.get('amount', transaction.amount)
        transaction.category = data.get('category', transaction.category)
        transaction.description = data.get('description', transaction.description)

        db.session.commit()

        return make_response(jsonify({'message': 'Transaction updated successfully'}), 200)

    @app.route('/transactions/<int:id>', methods=['DELETE'])
    def delete_transaction(id):
        transaction = Transaction.query.get(id)
        if not transaction:
            return make_response(jsonify({'message': 'Transaction not found'}), 404)

        db.session.delete(transaction)
        db.session.commit()

        return make_response(jsonify({'message': 'Transaction deleted successfully'}), 200)

    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({'message': 'User deleted successfully'}), 200)
