from flask import current_app
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.user_model import User
from app.models.auth_model import Auth
from app.third_parties.telegram.send_new_user_notification import send_new_user_notification
from app.utils.exceptions import appConflictError


def execute(username, email, password, role="client", created_by="system"):
    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        raise appConflictError('Username already exists')

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        raise appConflictError('Email already exists')

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        created_by=created_by
    )

    # Save the user to the database and provide a default created_by
    new_user.save(is_new=True)  # Passing is_new=True because it's a new record

    # Create a new auth record linked to the user
    new_auth = Auth(
        username=username,
        password=hashed_password,
        email=email,
        role=role,
        user_id=new_user.id  # Link the Auth record to the User record
    )

    # Save the auth record, passing the created_by field as 'system' or another admin
    new_user.save(is_new=True)

    chat_id = current_app.config['TELEGRAM_CHAT_ID']

    # Notify about the new user
    send_new_user_notification(username, chat_id)

    return dict(message='User registered successfully')
