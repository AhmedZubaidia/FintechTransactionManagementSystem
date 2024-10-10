from marshmallow import Schema, fields, validate


# Schema for registering a new user
class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=80)])
    email = fields.Email(required=True, validate=[validate.Length(min=1, max=120)])
    password = fields.Str(required=True, validate=[validate.Length(min=6)])


# Schema for logging in a user
class LoginSchema(Schema):
    email = fields.Email(required=True, validate=[validate.Length(min=1, max=120)])
    password = fields.Str(required=True, validate=[validate.Length(min=6)])


class UserSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(load_only=True)
    username = fields.Str()
    email = fields.Email()
    full_name = fields.Str()
    age = fields.Int()
    gender = fields.Str(validate=[validate.Length(max=10)])
    address = fields.Str(validate=[validate.Length(max=255)])
    phone_number = fields.Str(validate=[validate.Length(max=20)])
    profile_picture = fields.Str(validate=[validate.Length(max=255)])
    preferred_language = fields.Str(validate=[validate.Length(max=10)])
    currency = fields.Str(validate=[validate.Length(max=10)])
    deleted_at = fields.DateTime(required=False)


class ListUsers(Schema):
    page = fields.Int(load_only=True, load_default=1)
    per_page = fields.Int(load_only=True, load_default=10, validate=[validate.Range(min=1, max=50)])
    items = fields.List(fields.Nested(UserSchema), dump_only=True)
    pagination = fields.Dict(dump_only=True)
