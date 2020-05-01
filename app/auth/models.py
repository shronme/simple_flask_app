import secrets
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.cf_mixin import db, CFMixin


class APIKey(db.Model, CFMixin):
    __tablename__ = "api_keys"
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creation_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(120), nullable=False,
                       default='enabled')
    key = db.Column(db.String(120), nullable=False)
    owner = db.Column(db.String(120), nullable=False,
                      default='stride')

    def __init__(self):
        self.creation_date = datetime.now()
        self.status = 'enabled'
        self.key = secrets.token_urlsafe(64)
        self.save()

    def disable_key(self):
        self.status = 'disabled'
        self.save()
