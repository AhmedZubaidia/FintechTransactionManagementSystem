from marshmallow import Schema, fields


class MessageSchema(Schema):
    message = fields.Str(required=True)
