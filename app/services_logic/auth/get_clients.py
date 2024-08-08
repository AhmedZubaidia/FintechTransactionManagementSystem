from app.models.user import User

def execute():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return users_list, 200

def get_user_by_id(user_id):
    return User.query.get(user_id)
