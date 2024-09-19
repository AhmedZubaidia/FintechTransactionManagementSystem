from flask_jwt_extended import get_jwt_identity
from app.models.user_model import User
from app import db


def execute(**data):
    user_id = get_jwt_identity()  # Get the user's ID from the JWT token
    user = User.query.get(user_id)

    if not user:
        return dict(errors="User not found"), 404

    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    return dict(message="Profile updated successfully", user_id=user.id)
