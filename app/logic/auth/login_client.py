from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user import User
from app.third_parties.telegram.send_login_notification import send_login_notification
from app.utils.exceptions import appLoginError


def execute(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        # Send a login notification via Telegram
        chat_id = current_app.config['TELEGRAM_CHAT_ID']
        send_login_notification(user.username, chat_id)

        # Create the access token with only the user ID
        access_token = create_access_token(identity=user.id)

        # Save the encrypted user_id from the JWT token (if needed)
        user.save(jwt_token=access_token)  # Assuming you handle JWT in the save method

        # Return a dictionary with a success message and the JWT token
        return dict(message='Login successful', access_token=access_token)

    # Raise an exception if the email or password is incorrect
    raise appLoginError('Invalid email or password')
