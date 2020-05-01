from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask import current_app
from app.cf_mixin import CFMixin, db


class UserAccount(db.Model, CFMixin):
    __tablename__ = "user_account"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(120), nullable=False,
                           default='blank')
    last_name = db.Column(db.String(120),  nullable=False,
                          default='blank')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User {} with password {}>'.format(self.email, self.password)

    def set_password(self, password):
        self.password = \
            current_app.bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return current_app.bcrypt.check_password_hash(self.password, password)


class BlacklistToken(db.Model, CFMixin):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def is_token_blacklisted(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
