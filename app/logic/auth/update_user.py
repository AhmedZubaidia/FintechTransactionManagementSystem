from flask import has_request_context
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User
from app.utils.exceptions import appNotFoundError, appConflictError


def execute(user_id, username=None, email=None, password=None):
    # Find the user by ID
    user = User.query.get(user_id)
    if not user:
        raise appNotFoundError('User not found')

    # Check if the new username already exists (if it's being updated)
    if username and username != user.username:
        if User.query.filter_by(username=username).first():
            raise appConflictError('Username already exists')

    # Check if the new email already exists (if it's being updated)
    if email and email != user.email:
        if User.query.filter_by(email=email).first():
            raise appConflictError('Email already exists')

    # Update user details if provided
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # If within a request context, update the `modified_by` field with the JWT identity
    if has_request_context():
        try:
            current_user_id = get_jwt_identity()
            user.modified_by = current_user_id  # Use the ID from the JWT token
        except Exception as e:
            raise RuntimeError("JWT identity not available. Ensure this method is called in a request context.")
    else:
        raise RuntimeError("Request context is required to update modified_by.")

    db.session.commit()

    return dict(message='User updated successfully')
