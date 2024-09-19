from flask_jwt_extended import get_jwt_identity
from app.models.user_model import User
from app.schemas.user_schema import UserSchema


def execute():
    user_id = get_jwt_identity()  # Get the user's ID from the JWT token
    user = User.query.get(user_id)

    if not user:
        return dict(errors="User not found"), 404

    return UserSchema().dump(user)
