from functools import wraps
from flask import request, make_response, jsonify, current_app
from app.auth.models import APIKey


def require_auth(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if current_app.config['API_AUTH']:
            api_key = APIKey.query.all()[0].key
        else:
            api_key = 'test_api_key'

        # if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') \
           and request.headers.get('x-api-key') == api_key:
            return view_function(*args, **kwargs)
        else:
            responseObject = {
                    'status': 'fail',
                    'message': 'Unauthorised'
            }
            return make_response(jsonify(responseObject)), 401
    return decorated_function
