from app.models.user_model import User
from app.schemas.user_schema import UserSchema


def execute(page, per_page):
    page = int(page)
    per_page = int(per_page)

    users_query = User.query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize the user items
    users = UserSchema(many=True).dump(users_query.items)

    # Determine the next page URL, if applicable
    next_page = page + 1 if users_query.has_next else None

    # Return both the serialized users, pagination metadata, and next page
    return {
        'items': users,  # The paginated list of users
        'pagination': {
            'total': users_query.total,       # Total number of users
            'page': users_query.page,         # Current page
            'pages': users_query.pages,       # Total number of pages
            'per_page': users_query.per_page, # Users per page
            'next_page': next_page            # The next page number, or None if no next page
        }
    }
