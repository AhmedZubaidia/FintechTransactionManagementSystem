from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.auth_model import Auth
from app.models.user_model import User
from app.third_parties.telegram.send_login_notification import send_login_notification
from app.utils.exceptions import appLoginError

from flask import current_app


def execute(email, password):
    user = User.query.filter_by(email=email).first()
    auth = Auth.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        chat_id = current_app.config['TELEGRAM_CHAT_ID']
        send_login_notification(user.username, chat_id)

        additional_claims = {
            "username": user.username,
            "email": user.email,
            "role": auth.role.value,
        }

        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

        return dict(message='Login successful', access_token=access_token)

    raise appLoginError('Invalid email or password')
