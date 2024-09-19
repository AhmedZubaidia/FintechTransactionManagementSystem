import traceback
from functools import wraps
from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from jwt import ExpiredSignatureError
from app.third_parties.telegram.send_long_message import send_long_message
from app.utils.exceptions import ApplicationError, appForbiddenError, appBadRequestError
from math import ceil  # For calculating total pages


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

                # Only attempt to load JSON data if Content-Type is 'application/json'
                if request.content_type == 'application/json':
                    data = request.get_json() or {}
                elif request.method in ['POST', 'PUT', 'PATCH']:  # Methods that typically expect a body
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

                # If pagination is enabled, get page and per_page parameters
                if paginate:
                    try:
                        page = max(int(request.args.get('page', 1)), 1)  # Default to 1, must be positive
                        per_page = max(int(request.args.get('per_page', 10)), 1)  # Default to 10, must be positive
                    except ValueError:
                        raise appBadRequestError("Page and per_page must be valid positive integers.")

                    response, total_items = f(data, page, per_page)

                    # Calculate total pages and add pagination metadata
                    total_pages = ceil(total_items / per_page)
                    paginated_response = {
                        "items": response,
                        "pagination": {
                            "current_page": page,
                            "per_page": per_page,
                            "total_pages": total_pages,
                            "total_items": total_items
                        }
                    }
                    response = paginated_response

                elif request.method in ['DELETE', 'GET']:
                    # Don't require JSON, just use URL parameters
                    data = request.args.to_dict()

                # Only pass `data` to the function if it's not a DELETE request
                if request.method == 'DELETE':
                    response = f(**kwargs)  # No `data` for DELETE

                else:
                    response = f(**kwargs, data=data)  # Pass both kwargs and data to the function

                # Serialize the output using the schema if provided
                if not isinstance(response, dict):
                    response = schema(many=True if isinstance(response, list) else False).dump(response)

                # Determine the appropriate status code based on context or keys in response
                status_code = 200  # Default to 200 OK

                return make_response(jsonify(response), status_code)

            except ExpiredSignatureError:
                return make_response(jsonify({'errors': "Token has expired"}), 401)

            except ApplicationError as e:
                # Handle custom application errors
                return make_response(jsonify({'errors': str(e)}), e.status_code)

            except Exception as e:
                # For any unexpected errors, log and return a generic 500 error
                chat_id = "@erorr_notifaction"
                tb = traceback.format_exc()
                error_message = f"An unexpected error occurred: {str(e)}\nTraceback:\n{tb}"
                send_long_message(error_message, chat_id)

                return make_response(jsonify({'errors': "An unexpected error occurred"}), 500)

        bp.add_url_rule(rule, f.__name__, wrapped, **options)
        return wrapped

    return decorator
