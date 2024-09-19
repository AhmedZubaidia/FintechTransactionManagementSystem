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
