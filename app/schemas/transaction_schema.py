from marshmallow import Schema, fields, validate
from app.schemas.user_schema import UserSchema


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    category = fields.Str(required=True, validate=[validate.Length(min=1, max=50)])
    description = fields.Str(validate=[validate.Length(max=200)])
    type = fields.Str(required=True, validate=[validate.OneOf(["income", "expense"])])
    timestamp = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
