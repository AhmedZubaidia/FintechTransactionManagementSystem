from flask import current_app
from werkzeug.security import generate_password_hash

from app import db
from app.models.user import User
from app.third_parties.telegram.send_new_user_notification import send_new_user_notification
from app.utils.exceptions import ConflictError


def execute(username, email, password):
    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        raise ConflictError('Username already exists')

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        raise ConflictError('Email already exists')

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    chat_id = current_app.config['TELEGRAM_CHAT_ID']

    # Notify about the new user
    send_new_user_notification(username,chat_id)

    return dict(message='User registered successfully')
