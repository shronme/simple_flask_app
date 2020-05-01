from flask import Blueprint
from flask.views import MethodView

general_blueprint = Blueprint('general', __name__)


class GeneralViews(MethodView):
    def get(self):
        return 'Hello World :)'


general_view = GeneralViews.as_view('general_api')

general_blueprint.add_url_rule(
    '/',
    view_func=general_view,
    methods=['get']
)
