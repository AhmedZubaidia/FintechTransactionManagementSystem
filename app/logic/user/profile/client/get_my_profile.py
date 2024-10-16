from flask_jwt_extended import get_jwt_identity
from app.models.user_model import User
from app.schemas.user_schema import UserSchema
from app.utils.exceptions import appNotFoundError


def execute(user_id):

    user = User.query.get(user_id)
    if not user or user.deleted_at:
        raise appNotFoundError(f"User with ID {user_id} not found")

    return user
