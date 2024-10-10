import traceback
from functools import wraps
from flask import request, jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from jwt import ExpiredSignatureError
import inspect
from app.schemas.paginatedSchema import PaginatedSchema
from app.third_parties.telegram.send_long_message import send_long_message
from app.utils.exceptions import appForbiddenError, appBadRequestError, ApplicationError
from marshmallow import ValidationError


def custom_route(bp, rule, *, schema=None, require_auth=False, allowed_roles=None, paginate=False,
                 append_token_key=None, **options):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                # If authentication is required, verify the JWT first
                user_id = None
                if require_auth:
                    verify_jwt_in_request()
                    user_id = get_jwt_identity()

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

                if append_token_key:
                    for key in append_token_key:
                        if key == 'user_id' and user_id:
                            data['user_id_token'] = user_id

                if paginate:
                    data = PaginatedSchema(item_schema=schema).load(data)
                else:
                    data = schema().load(data)

                # Check if `f` accepts arguments using `inspect.signature`
                func_signature = inspect.signature(f)
                valid_params = func_signature.parameters.keys()

                args = []
                kwargs = {}

                if 'data' in valid_params:
                    args.append(data)
                response = f(*args, **kwargs) if len(func_signature.parameters) > 0 else f()

                if paginate:
                    page = int(data.get('page', 1))
                    per_page = int(data.get('per_page', 10))

                    # Ensure the response is a pagination object with .items and .total
                    total_items = response.total if hasattr(response, 'total') else len(response)

                    # Serialize the items using the provided schema (assuming `schema` is passed)
                    items = schema(many=True).dump(response.items if hasattr(response, 'items') else response)

                    # Create pagination metadata using the PaginatedSchema static method
                    pagination = PaginatedSchema.generate_pagination_metadata(page, per_page, total_items)

                    response = {
                        'items': items,
                        'pagination': pagination
                    }

                if not isinstance(response, dict):
                    response = schema(many=True if isinstance(response, list) else False).dump(response)

                return make_response(jsonify(response), 200)


            except ExpiredSignatureError:
                return make_response(jsonify({'errors': 'Access forbidden: token expired'}), 401)

            except ApplicationError as e:

                return make_response(jsonify({'errors': str(e)}), e.status_code)

            except ValueError as e:
                return make_response(jsonify({'errors': str(e)}), 400)


            except Exception as e:

                tb = traceback.format_exc()

                error_message = f"An unexpected error occurred: {str(e)}\nTraceback:\n{tb}"

                send_long_message(error_message, "@erorr_notifaction")

                return make_response(jsonify({'errors': "An unexpected error occurred"}), 500)

        bp.add_url_rule(rule, f.__name__, wrapped, **options)
        return wrapped

    return decorator
