from werkzeug.security import check_password_hash
from app.models.user import User
from app.third_parties.telegram.send_login_notification import send_login_notification

def execute(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        send_login_notification(user.username)
        return user, 200
    return {'message': 'Login failed'}, 401
