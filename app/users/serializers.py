from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import field_for
from marshmallow import ValidationError, validate
from app import validators
from app.users.models import (
    UserAccount
)

ma = Marshmallow()


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided')


class UserSchema(ma.ModelSchema):

    email = field_for(UserAccount, 'email', required=True, validate=[
        must_not_be_blank,
        validate.Email(),
        validators.validate_email])

    password = field_for(UserAccount, 'password', required=True, validate=[
        must_not_be_blank,
        validators.validate_password])

    class Meta:
        model = UserAccount
