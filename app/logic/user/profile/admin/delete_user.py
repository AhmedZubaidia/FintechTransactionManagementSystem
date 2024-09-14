from app.models.user_model import User
from app import db


def execute(user_id):
    user = User.query.get(user_id)
    if not user:
        return dict(errors="User not found"), 404

    db.session.delete(user)
    db.session.commit()

    return dict(message="User deleted successfully")
