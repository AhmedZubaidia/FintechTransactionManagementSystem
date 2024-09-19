from app.models.user_model import User
from app.schemas.user_schema import UserSchema


def execute(page, per_page):
    users_query = User.query.paginate(page=page, per_page=per_page, error_out=False)

    users = UserSchema(many=True).dump(users_query.items)

    return users, users_query.total  # Return total items for pagination metadata
