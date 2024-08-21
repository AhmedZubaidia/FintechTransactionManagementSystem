from flask import jsonify, make_response, request, current_app
from app import db
from app.models.user import User
from app.third_parties.telegram.send_user_deletion_notification import send_user_deletion_notification
from app.utils.exceptions import ProfileError


def execute(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ProfileError('User not found')

    db.session.delete(user)
    db.session.commit()
    chat_id = current_app.config['TELEGRAM_CHAT_ID']
    send_user_deletion_notification(user.username,chat_id )

    return dict(message='User deleted successfully')
