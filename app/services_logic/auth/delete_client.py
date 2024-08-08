from app import db
from app.third_parties.telegram.send_user_deletion_notification import send_user_deletion_notification


def execute(user):
    db.session.delete(user)
    db.session.commit()
    send_user_deletion_notification(user.username)
    return {'message': 'User deleted successfully'}, 200
