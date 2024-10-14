from app.models.user_model import User
from app import db


def execute(user_id, **data):
    user = User.query.get(user_id)
    if not user:
        return dict(errors="User not found")

    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    return dict(message="User updated successfully", user_id=user.id)
