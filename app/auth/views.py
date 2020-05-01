from flask import (
    Blueprint,
    request,
    make_response,
    jsonify,
    current_app
    )
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from flask.views import MethodView
from app.auth.decorators import (
    require_auth
)

from app.cf_mixin import db
from app.users.models import UserAccount, BlacklistToken
from app.helpers import get_auth_token

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    @require_auth
    def post(self):
        # get the post data
        data = request.get_json()
        # check if user already exists
        user = UserAccount.query.filter_by(email=data.get('email')).first()
        if not user:
            try:
                user = UserAccount(first_name=data['first_name'],
                                   last_name=data['last_name'],
                                   email=data['email'],
                                   password=data['password'])
                user.set_password(user.password)
                user.save()

                # generate the auth token
                auth_token = create_access_token(identity=user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token,
                    'user': '{} {}'.format(user.first_name, user.last_name)
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again: '
                              + str(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Failed to create this user.',
            }
            return make_response(jsonify(responseObject)), 400


# TODO add user object in login and register
class LoginAPI(MethodView):
    """
    User Login Resource
    """
    @require_auth
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = UserAccount.query.filter_by(
                email=post_data.get('email')
              ).first()

            if user and current_app.bcrypt.check_password_hash(
                user.password, post_data.get('password')
            ):
                auth_token = create_access_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token,
                        'user': '{} {}'.format(user.first_name, user.last_name)
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Invalid Token.'
                    }
                    return make_response(jsonify(responseObject)), 404
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Login failed'
                }
                return make_response(jsonify(responseObject)), 404

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    User Resource
    """
    @jwt_required
    def get(self):
        # get the auth token
        auth_token = get_auth_token(request)
        if auth_token:
            resp = get_jwt_identity()
            if not BlacklistToken.is_token_blacklisted(auth_token):

                if resp:
                    user = UserAccount.query.filter_by(id=resp).first()

                    responseObject = {
                        'status': 'success',
                        'data': {
                            'user_id': user.id,
                            'email': user.email
                        }
                    }
                    return make_response(jsonify(responseObject)), 200
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Token Expired'
                }
                return make_response(jsonify(response_object)), 401

        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    @jwt_required
    def post(self):
        # get auth token
        auth_token = get_auth_token(request)
        if auth_token:
            resp = get_jwt_identity()
            if not BlacklistToken.is_token_blacklisted(auth_token):
                if resp:
                    # mark the token as blacklisted
                    blacklist_token = BlacklistToken(token=auth_token)
                    try:
                        # insert the token
                        db.session.add(blacklist_token)
                        db.session.commit()
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged out.'
                        }
                        return make_response(jsonify(responseObject)), 200
                    except Exception as e:
                        responseObject = {
                            'status': 'fail',
                            'message': e
                        }
                        return make_response(jsonify(responseObject)), 401
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': resp
                    }
                    return make_response(jsonify(responseObject)), 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Token Expired'
                }
                return make_response(jsonify(response_object)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


class ResetPasswordRequestAPI(MethodView):
    """
    Reset password request resources
    """
    @require_auth
    def post(self):
        data = request.get_json()
        # check if user already exists
        user = UserAccount.query.filter_by(email=data.get('email')).first()
        if user:
            token = create_access_token(identity=user.id)
            SendgridClient().reset_password_email(user.email, token)
        responseObject = {
            'status': 'success',
            'message': 'Password reset request accepted'
        }
        return make_response(jsonify(responseObject)), 200


class ResetPasswordAPI(MethodView):
    """
    Reset password resources
    """
    @jwt_required
    def post(self):
        data = request.get_json()
        auth_token = get_auth_token(request)
        if auth_token:
            resp = get_jwt_identity()
            if not BlacklistToken.is_token_blacklisted(auth_token):
                if resp:
                    user = UserAccount.query.filter_by(id=resp).first()
                    new_password = data['password']
                    user.set_password(new_password)
                    user.save()
                    blacklist_token = BlacklistToken(token=resp)
                    blacklist_token.save()
                    auth_token = create_access_token(identity=user.id)
                    responseObject = {
                        'status': 'success',
                        'message': 'Password updated',
                        'auth_token': auth_token,
                        'user': '{} {}'.format(user.first_name, user.last_name)
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Token Expired'
                }
                return make_response(jsonify(response_object)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_view')
user_view = UserAPI.as_view('user_api')
reset_password_request_view = ResetPasswordRequestAPI.as_view(
    'reset_password_request_api')
reset_password_view = ResetPasswordAPI.as_view('reset_password_api')


# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/reset_password_request',
    view_func=reset_password_request_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/reset_password',
    view_func=reset_password_view,
    methods=['POST']
)
