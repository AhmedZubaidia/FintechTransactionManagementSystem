import traceback
from functools import wraps
from flask import request, jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from jwt import ExpiredSignatureError
from math import ceil

from app.third_parties.telegram.send_long_message import send_long_message
from app.utils.exceptions import appForbiddenError, appBadRequestError, ApplicationError


def custom_route(bp, rule, *, schema=None, require_auth=False, allowed_roles=None, paginate=False, **options):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                # If authentication is required, verify the JWT first
                if require_auth:
                    verify_jwt_in_request()

                    # Role-based access control
                    if allowed_roles is not None:
                        jwt_data = get_jwt()
                        user_role = jwt_data.get('role', None)
                        if user_role not in allowed_roles:
                            raise appForbiddenError("Access forbidden: insufficient permissions")

                data = {}

                # Only load JSON data if Content-Type is 'application/json'
                if request.content_type == 'application/json':
                    data = request.get_json() or {}
                elif request.method in ['POST', 'PUT', 'PATCH']:  # Methods that require a body
                    raise appBadRequestError("Content-Type must be 'application/json'")

                # Add URL parameters (kwargs)
                data.update(kwargs)

                # Add query string parameters (request.args)
                data.update(request.args.to_dict())

                # Handle file uploads
                files = request.files.to_dict()
                data.update(files)

                # Validate and deserialize the input data if a schema is provided
                if schema:
                    data = schema().load(data)

                response = f(data)

                if not isinstance(response, dict):
                    response = schema(many=True if isinstance(response, list) else False).dump(response)

                return make_response(jsonify(response), 200)


            except ExpiredSignatureError:
                return make_response(jsonify({'errors': 'Access forbidden: token expired'}), 401)

            except ApplicationError as e:

                return make_response(jsonify({'errors': str(e)}), e.status_code)


            except Exception as e:

                tb = traceback.format_exc()

                error_message = f"An unexpected error occurred: {str(e)}\nTraceback:\n{tb}"

                send_long_message(error_message, "@erorr_notifaction")

                return make_response(jsonify({'errors': "An unexpected error occurred"}), 500)

        bp.add_url_rule(rule, f.__name__, wrapped, **options)
        return wrapped

    return decorator
