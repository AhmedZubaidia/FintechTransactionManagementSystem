from werkzeug.security import generate_password_hash
from app.models.user import User
from app import db
from app.third_parties.telegram.send_new_user_notification import send_new_user_notification

def execute(username, email, password):
    if User.query.filter_by(username=username).first():
        return {'message': 'Username already exists'}, 400
    if User.query.filter_by(email=email).first():
        return {'message': 'Email already exists'}, 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    send_new_user_notification(username)

    return {'message': 'User registered successfully'}, 201
