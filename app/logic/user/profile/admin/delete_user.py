from app.models.user_model import User
from app import db
from datetime import datetime


def execute(user_id):
    user = User.query.get(user_id)
    if not user:
        return dict(errors="User not found")

    if user.is_deleted:
        return dict(errors="User is already deleted")

    # Soft delete the user
    user.deleted_at = datetime.utcnow()
    db.session.commit()

    return dict(message="User soft deleted successfully")
