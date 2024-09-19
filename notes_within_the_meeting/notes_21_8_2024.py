# here we start with the notes of the meeting of 21st August 2024

#
# add information for jwt token and read it .
#
#
# Update deploy github action to handle only run once the pull-request against master got merged.
# Remove mysql from the deployment action.
# Ensure the image is deployed on docker.hub
#
#
#

# Milestone 2
# Auth model
# username, password, email, role, is_active, is_deleted, user_id, user_type (Client), last_login_at, last_login_ip # done
#
# Role: one of: admin, client
#
# User model
# full_name, age, gender, address, phone_number, profile_picture # done


# APIS:
# Login for admin
# Login for client
#      after logged in
#         get my profile
#         get my transactions
#
# CLint can only consume his api, and can not consume the admin api
# Admin Can consume admin apis
# allowed_roles = ['admin| client']


#
#
#
#
#
#
#9/
#
#
#
#
#
#
#
#
#

