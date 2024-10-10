from flask_jwt_extended import get_jwt_identity
from app.models.user_model import User
from app import db


def execute(**data):
    # Get the user_id from **data
    user_id = data.get("user_id")
    user = User.query.get(user_id)

    if not user or user.deleted_at:
        return dict(errors="User not found")

    # Ensure that email is not allowed to be changed
    if "email" in data:
        return dict(errors="Changing email is not allowed")

    # Check if the username is unique (if it's being changed)
    new_username = data.get("username")
    if new_username and new_username != user.username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            return dict(errors="Username is already taken")

    # Update the user's other fields
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()

    return dict(message="Profile updated successfully", user_id=user.id)
