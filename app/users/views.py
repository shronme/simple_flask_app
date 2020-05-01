# from flask import (
#     Blueprint,
#     request,
#     make_response,
#     jsonify,
#     )
# from flask_jwt_extended import (
#     jwt_required,
#     get_jwt_identity
# )
# from flask.views import MethodView
# from app.auth.decorators import (
#     require_auth
# )
# from app.users.models import (
#     User,
#     BlacklistToken
#     )
# from app.Users.serializers import (
#     StrideUserSchema,
#     ProfileSchema
#     )
# from app.helpers import get_auth_token
# from integrations.airtable import AirTableClient

# stride_User_blueprint = Blueprint('stride_User', __name__)
# profile_blueprint = Blueprint('profile', __name__)
# profile_suggestion_blueprint = Blueprint('Profile Suggestion', __name__)
# balances_blueprint = Blueprint('balances', __name__)
# update_balances_blueprint = Blueprint('update_balance', __name__)


# class StrideUserAPI(MethodView):
#     """
#     Creating a stride account for a user
#     """

#     @jwt_required
#     def post(self):
#         token = get_auth_token(request)
#         resp = get_jwt_identity()
#         if not BlacklistToken.is_token_blacklisted(token):
#             user = User.query.filter_by(id=resp).first()
#             if user:
#                 if user.stride_account_id:
#                     response_object = {
#                         'status': 'fail',
#                         'message': 'User already has stride account.'
#                         }
#                     return make_response(jsonify(response_object)), 403
#                 else:
#                     stride_account = StrideAccount()
#                     stride_account.users.append(user)
#                     stride_account.save()

#                     response_object = {
#                         'status': 'success',
#                         'data': {
#                             'stride_account': stride_account.id
#                         }
#                     }
#                     return make_response(jsonify(response_object), 201)
#             else:
#                 response_object = {
#                         'status': 'fail',
#                         'message': 'User does not exist'
#                         }
#                 return make_response(jsonify(response_object)), 403
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401

#     @jwt_required
#     def get(self, pk):
#         token = get_auth_token(request)
#         if not BlacklistToken.is_token_blacklisted(token):
#             stride_account = StrideAccount.query.filter_by(id=pk).first()
#             if stride_account:
#                 stride_account_schema = StrideAccountSchema()
#                 response_object = {
#                     'status': 'success',
#                     'data': stride_account_schema.dump(stride_account)
#                 }
#                 return make_response(jsonify(response_object)), 200
#             else:
#                 response_object = {
#                     'status': 'fail',
#                     'message': 'Account does not exist'
#                 }
#                 return make_response(jsonify(response_object)), 403
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401


# class ProfileAPI(MethodView):
#     """
#     API for creating profiles
#     """
#     @jwt_required
#     def post(self):
#         data = request.get_json()
#         resp = get_jwt_identity()
#         token = get_auth_token(request)
#         if not BlacklistToken.is_token_blacklisted(token):
#             user = Account.query.filter_by(id=resp).first()
#             stride_account = user.stride_account
#             if stride_account:
#                 profile = Profile(data, stride_account.id)

#                 if profile.money_account == {}:
#                     response_object = {
#                         'status': 'fail',
#                         'message': 'profile data invalid'
#                     }
#                     return make_response(jsonify(response_object)), 403
#                 else:
#                     stride_account.profiles.append(profile)
#                     stride_account.save()
#                     profile.save()

#                     response_object = {
#                         'status': 'success',
#                         'message': 'Profile Created'
#                     }
#                     return make_response(jsonify(response_object)), 201
#             else:
#                 response_object = {
#                         'status': 'fail',
#                         'message': 'No stride account'
#                     }
#                 return make_response(jsonify(response_object)), 403
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401

#     """
#     API for retrieving profiles
#     """
#     @jwt_required
#     def get(self):
#         resp = get_jwt_identity()
#         token = get_auth_token(request)
#         if not BlacklistToken.is_token_blacklisted(token):
#             user = Account.query.filter_by(id=resp).first()
#             stride_account = user.stride_account
#             profile_list = []
#             for profile in stride_account.profiles:
#                 profile_schema = ProfileSchema()
#                 profile_json = profile_schema.dump(profile)
#                 profile_total_balance = \
#                     profile.get_profile_balances()['total_balance']
#                 profile_json['profile_balance'] = profile_total_balance
#                 profile_list.append(profile_json)
#             response_object = {
#                 'status': 'success',
#                 'data': profile_list
#             }
#             return make_response(jsonify(response_object)), 200
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401

#     """
#     API for editing a profile
#     """
#     @jwt_required
#     def patch(self, pk):
#         token = get_auth_token(request)
#         if not BlacklistToken.is_token_blacklisted(token):
#             data = request.get_json()
#             profile = Profile.query.filter_by(id=pk).first()
#             profile.update_profile(data)
#             response_object = {
#                         'status': 'success',
#                         'message': 'Profile Updated'
#                 }
#             return make_response(jsonify(response_object)), 202
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401

#     """
#     API for deleting a profile
#     """
#     @jwt_required
#     def delete(self, pk):
#         profile = Profile.query.filter_by(id=pk).first()
#         if profile:
#             try:
#                 profile.delete_profile()
#                 response_object = {
#                             'status': 'success',
#                             'message': 'Profile Updated'
#                     }
#                 return make_response(jsonify(response_object)), 200
#             except Exception:
#                 response_object = {
#                     'status': 'Failed',
#                     'message': 'failed to delete profile'
#                 }
#                 return make_response(jsonify(response_object)), 404
#         else:
#             response_object = {
#                 'status': 'Failed',
#                 'message': 'failed to delete profile'
#             }
#             return make_response(jsonify(response_object)), 404


# class BalancesAPI(MethodView):
#     """
#     API for getting all the balances
#     """
#     @jwt_required
#     def get(self):
#         resp = get_jwt_identity()
#         token = get_auth_token(request)
#         if not BlacklistToken.is_token_blacklisted(token):
#             user = Account.query.filter_by(id=resp).first()
#             account_balances = {'balances': []}

#             if user:
#                 stride_account_total_balance = 0
#                 if user.stride_account_id:
#                     profiles = StrideAccount.query.filter_by(
#                         id=user.stride_account_id).first().profiles
#                     for profile in profiles:
#                         profile_balances = profile.get_profile_balances()
#                         stride_account_total_balance += \
#                             profile_balances['total_balance']
#                         account_balances['balances'].append(profile_balances)
#                     account_balances['total_account_balance'] = \
#                         stride_account_total_balance
#                 response_object = {
#                     'status': 'success',
#                     'data': account_balances
#                 }
#                 return make_response(jsonify(response_object)), 200
#             else:
#                 response_object = {
#                         'status': 'fail',
#                         'message': 'No stride account'
#                     }
#                 return make_response(jsonify(response_object)), 403
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401


# class BalanceUpdateAPI(MethodView):
#     """
#     updating balance for account
#     """
#     @require_auth
#     def post(self):
#         analyze_profiles.apply_async()

#         response_object = {
#             'status': 'success',
#             'message': ''
#         }
#         return make_response(jsonify(response_object), 200)


# class ProfileSuggestAPI(MethodView):
#     """
#     API for suggesting new vendors
#     """
#     @jwt_required
#     def post(self):
#         user_id = get_jwt_identity()
#         data = request.get_json()
#         token = get_auth_token(request)
#         if not BlacklistToken.is_token_blacklisted(token):
#             user = Account.query.filter_by(id=user_id).first()
#             if user:
#                 at_client = AirTableClient()
#                 response = at_client.update_vendor_suggestion(user_id, data)
#                 if response.status_code == 200:
#                     response_object = {
#                         'status': 'success',
#                         'message': 'suggestion updated'
#                     }
#                     return make_response(jsonify(response_object), 200)
#                 else:
#                     response_object = {
#                         'status': 'failed',
#                         'message': 'suggestion update failed'
#                     }
#                     return make_response(jsonify(response_object), 400)
#             else:
#                 response_object = {
#                     'status': 'failed',
#                     'message': 'User not found'
#                 }
#                 return make_response(jsonify(response_object), 400)
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Token Expired'
#             }
#             return make_response(jsonify(response_object)), 401


# balance_update_view = BalanceUpdateAPI.as_view('balance_update_api')
# update_balances_blueprint.add_url_rule(
#     '/profile_balance',
#     view_func=balance_update_view,
#     methods=['POST']
# )

# profile_view = ProfileAPI.as_view('profile_api')
# profile_blueprint.add_url_rule(
#     '/profile',
#     view_func=profile_view,
#     methods=['POST']
# )
# profile_blueprint.add_url_rule(
#     '/profile',
#     view_func=profile_view,
#     methods=['GET']
# )
# profile_blueprint.add_url_rule(
#     '/profile/<pk>',
#     view_func=profile_view,
#     methods=['PATCH']
# )
# profile_blueprint.add_url_rule(
#     '/profile/<pk>',
#     view_func=profile_view,
#     methods=['DELETE']
# )

# account_view = StrideAccountAPI.as_view('stride_account_api')
# stride_account_blueprint.add_url_rule(
#     '/account/<pk>',
#     view_func=account_view,
#     methods=['GET']
# )
# stride_account_blueprint.add_url_rule(
#     '/account',
#     view_func=account_view,
#     methods=['POST']
# )

# balances_view = BalancesAPI.as_view('balances_api')
# balances_blueprint.add_url_rule(
#     '/balances',
#     view_func=balances_view,
#     methods=['GET']
# )

# profile_suggestion_view = ProfileSuggestAPI.as_view('profile_suggestion_api')
# profile_suggestion_blueprint.add_url_rule(
#     '/profile_suggestion',
#     view_func=profile_suggestion_view,
#     methods=['POST']
# )
