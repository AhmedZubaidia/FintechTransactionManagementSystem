from marshmallow import Schema, fields, validate
from app.models.transaction_model import TransactionCategory, TransactionType


# Schema for representing a transaction without any user details
class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    category = fields.Str(
        required=True,
        validate=validate.OneOf([category.value for category in TransactionCategory])  # Enum validation for category
    )
    description = fields.Str(validate=[validate.Length(max=200)])
    type = fields.Str(
        required=True,
        validate=validate.OneOf([type_.value for type_ in TransactionType])  # Enum validation for type (credit/debit)
    )
    timestamp = fields.DateTime(dump_only=True)
