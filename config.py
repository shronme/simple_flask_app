import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    API_AUTH = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # CREDENTIALS_SECRET = os.environ['CREDENTIALS_SECRET']
    # CREDENTIALS_SALT = os.environ['CREDENTIALS_SALT']
    # REDIS_HOST = os.environ['REDIS_HOST']
    # REDIS_PORT = os.environ['REDIS_PORT']
    # FROM_ADDRESS = os.environ['FROM_ADDRESS']
    # SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
    # BROKER_URL = 'redis://{host}:{port}/0'.format(
    #     host=REDIS_HOST, port=str(REDIS_PORT))
    # CELERY_RESULT_BACKEND = BROKER_URL
    # CELERY_BROKER_URL = BROKER_URL
    # # CELERY_IMPORTS = ('app.accounts.tasks')
    # CELERY_TASK_RESULT_EXPIRES = 30
    # CELERY_TIMEZONE = 'UTC'

    # CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    # CELERY_TASK_SERIALIZER = 'json'
    # CELERY_RESULT_SERIALIZER = 'json'

    SQLALCHEMY_ENGINE_OPTIONS = {
        'isolation_level': 'AUTOCOMMIT'
    }


class ProductionConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    API_AUTH = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    API_AUTH = False
