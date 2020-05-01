from flask import (
    Blueprint,
    request,
    make_response,
    jsonify
    )
from app.auth.decorators import (
    require_auth
)

from flask.views import MethodView
from app.helpers import get_auth_token

data_sources_blueprint = Blueprint('data_sources', __name__)


class FinancialFileAPI(MethodView):
    """
    API to receive financial files from Vantage
    """

    @require_auth
    def post(self, pk):
        
        try:
            if 'financial_file' in request.files:
                print('OK')
                responseObject = {
                    'status': 'success',
                    'message': 'File received'
                }
                return make_response(jsonify(responseObject)), 200
            else:
                print('No ok')
        except KeyError as e:
            response_object = {
                'status': 'fail',
                'message': 'No files in request: ' + e
            }
            return make_response(jsonify(response_object)), 401


financial_file_view = FinancialFileAPI.as_view('financial_file')

data_sources_blueprint.add_url_rule(
    '/data_sources/financial_file',
    view_func=financial_file_view,
    methods=['POST']
)
