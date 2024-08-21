from marshmallow import Schema, fields, validate
from app.models.user import User

from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=80)])
    email = fields.Email(required=True, validate=[validate.Length(min=1, max=120)])
    password = fields.Str(required=True, validate=[validate.Length(min=6)])


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=[validate.Length(min=1, max=120)])
    password = fields.Str(required=True, validate=[validate.Length(min=6)])


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    transactions = fields.List(fields.Nested('TransactionSchema'), dump_only=True)
