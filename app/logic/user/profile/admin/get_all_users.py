from app.models.user_model import User
from app.schemas.user_schema import UserSchema


def execute(page, per_page):

    page = int(page)
    per_page = int(per_page)
    users_query = User.query.paginate(page=page, per_page=per_page, error_out=False)

    return users_query

