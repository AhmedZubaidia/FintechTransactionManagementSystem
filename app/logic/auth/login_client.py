from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user import User
from app.third_parties.telegram.send_login_notification import send_login_notification
from app.utils.exceptions import appLoginError


def execute(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        chat_id = current_app.config['TELEGRAM_CHAT_ID']
        send_login_notification(user.username, chat_id)
        access_token = create_access_token(identity=user.id)
        return dict(message=f'Login successful    {access_token}  ')

    raise appLoginError('Invalid email or password')
