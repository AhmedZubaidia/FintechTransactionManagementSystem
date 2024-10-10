from app.models.user_model import User
from app import db
from datetime import datetime


def execute(user_id):
    # Fetch the user from the database by user_id
    user = User.query.get(user_id)

    # Check if the user exists
    if not user:
        return dict(errors="User not found")

    # Check if the user is already deleted
    if user.deleted_at is not None:
        return dict(errors="User is already deleted")

    # Perform the soft delete by setting the deleted_at timestamp
    user.deleted_at = datetime.utcnow()
    db.session.commit()

    return dict(message="Profile soft deleted successfully")
