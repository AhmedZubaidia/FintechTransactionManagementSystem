from flask import current_app
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.user_model import User
from app.models.auth_model import Auth
from app.third_parties.telegram.send_new_user_notification import send_new_user_notification
from app.utils.exceptions import appConflictError


def execute(username, email, password, role="client"):
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
        created_by=username,
        modified_by=username  # Set created_by and modified_by to username initially
    )

    # Commit the new user to the database to generate the user ID
    db.session.add(new_user)
    db.session.commit()

    # Create a new auth record linked to the user
    new_auth = Auth(
        username=username,
        password=hashed_password,
        email=email,
        role=role,
        user_id=new_user.id  # Link the Auth record to the User record
    )

    # Commit the new auth record to the database
    db.session.add(new_auth)
    db.session.commit()

    # Generate a token for the user (for authentication purposes after registration)
    token_id = create_access_token(identity={
        'user_id': new_user.id,
        'role': new_auth.role.value
    })

    chat_id = current_app.config['TELEGRAM_CHAT_ID']

    # Notify about the new user
    send_new_user_notification(username, chat_id)

    return dict(message='User registered successfully')
