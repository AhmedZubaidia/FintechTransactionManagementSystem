from flask import Blueprint
from app.schemas.user_schema import UserSchema
from app.utils.custom_route import custom_route

bp = Blueprint('profile', __name__)


# Admin Route to get all users
@custom_route(bp, '/admin/users', methods=['GET'], schema=None, require_auth=True, allowed_roles="admin",
              paginate=True)
def get_all_users_admin(page, per_page):
    from app.logic.user.profile.admin.get_all_users import execute
    return execute(page, per_page)


# Admin Route to delete a user by ID
@custom_route(bp, '/admin/users/<int:id>', methods=['DELETE'], require_auth=True, allowed_roles="admin")
def delete_user_admin(id):  # Explicitly accept `id`
    from app.logic.user.profile.admin.delete_user import execute
    return execute(id)


# Admin Route to update a user by ID
@custom_route(bp, '/admin/users/<int:id>', methods=['PUT'], schema=UserSchema, require_auth=True, allowed_roles="admin")
def update_user_admin(id, data):
    from app.logic.user.profile.admin.update_user import execute
    return execute(id, **data)


@custom_route(bp, '/client/my-profile', methods=['GET'], require_auth=True, allowed_roles="client")
def get_my_profile_client(data):
    from app.logic.user.profile.client.get_my_profile import execute
    return execute()


# Client Route to update the profile of the current logged-in user
@custom_route(bp, '/client/my-profile', methods=['PUT'], schema=UserSchema, require_auth=True, allowed_roles="client")
def update_my_profile_client(data):
    from app.logic.user.profile.client.update_my_profile import execute
    return execute(**data)


# Client Route to delete the profile (mark as deleted) of the current logged-in user
@custom_route(bp, '/client/my-profile', methods=['DELETE'], require_auth=True, allowed_roles="client")
def delete_my_profile_client(data):
    from app.logic.user.profile.client.delete_my_profile import execute
    return execute()
