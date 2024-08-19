import traceback
from functools import wraps
from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required
from jwt import ExpiredSignatureError
from app.third_parties.telegram.send_long_message import send_long_message


def custom_route(bp, rule, *, schema=None, require_auth=False, **options):
    def decorator(f):
        if require_auth:
            f = jwt_required()(f)

        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                data = {}

                # Only attempt to load JSON data if Content-Type is 'application/json'
                if request.content_type == 'application/json':
                    data = request.get_json() or {}
                elif request.method in ['POST', 'PUT', 'PATCH']:  # Methods that typically expect a body
                    return make_response(jsonify({'errors': "Content-Type must be 'application/json'"}), 400)

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

                # Execute the original route function with the combined data
                response = f(data)

                # Serialize the output using the schema if provided
                if not isinstance(response, dict):
                    response = schema(many=True if isinstance(response, list) else False).dump(response)

                # Determine the appropriate status code based on context or keys in response
                status_code = 200  # Default to 200 OK

                return make_response(jsonify(response), status_code)

            except Exception as e:

                if isinstance(e, ExpiredSignatureError):
                    status_code = 401
                    error_message = "Token has expired"

                elif hasattr(e, 'is_application_error'):
                    status_code = getattr(e, 'status_code', 400)
                    error_message = str(e)

                else:
                    # For any unexpected errors, use a generic message and status code 500
                    chat_id = "@erorr_notifaction"

                    tb = traceback.format_exc()
                    error_message = f"An unexpected error occurred: {str(e)}\nTraceback:\n{tb}"
                    send_long_message(error_message, chat_id)

                    status_code = 500
                    error_message = "An unexpected error occurred"

                return make_response(jsonify({'errors': error_message}), status_code)

        bp.add_url_rule(rule, f.__name__, wrapped, **options)
        return wrapped

    return decorator
