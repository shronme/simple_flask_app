import os
from flask import Flask
from flask_bcrypt import Bcrypt
# from celery import Celery
from flask_cors import CORS
from app.cf_mixin import db
from app.data_sources.views import data_sources_blueprint
from app.auth.views import auth_blueprint
from app.views import general_blueprint
from app.auth.jwt_manager import jwt


def create_app():
    application = Flask(__name__)
    with application.app_context():
        application.config.from_object(os.environ['APP_SETTINGS'])

        # initialising database
        application.db = db
        application.db.init_app(application)
        application.db.create_all()

        application.bcrypt = Bcrypt(application)
        application.jwt = jwt.init_app(application)

        # registering blueprints
        application.register_blueprint(auth_blueprint)
        application.register_blueprint(general_blueprint)
        application.register_blueprint(data_sources_blueprint)

        application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        application.debug = application.config['DEBUG']
        CORS(application, resources={r"/*": {"origins": "*"}})
    return application


app = create_app()
