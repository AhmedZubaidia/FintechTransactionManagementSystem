from app.models.user_model import User
from app.schemas.user_schema import UserSchema


def execute():
    users = User.query.all()
    return UserSchema(many=True).dump(users)
