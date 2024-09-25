from marshmallow import Schema, fields, validate
from app.models.transaction_model import TransactionCategory, TransactionType


# Schema for representing a transaction without any user details
class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    amount = fields.Float(required=True, dump_only=True)
    category = fields.Str(
        required=True,
        dump_only=True,
        validate=validate.OneOf([category.value for category in TransactionCategory])  # Enum validation for category
    )
    description = fields.Str(validate=[validate.Length(max=200)])
    transaction_type = fields.Str(  # Updated 'type' to 'transaction_type'
        required=True,
        dump_only=True,
        validate=validate.OneOf([type_.value for type_ in TransactionType])
        # Enum validation for transaction type (credit/debit)
    )
    timestamp = fields.DateTime(dump_only=True)


class ListTransactionsSchema(Schema):
    page = fields.Int(load_only=True, load_default=1)
    per_page = fields.Int(load_only=True, load_default=10, validate=[validate.Range(min=1, max=50)])

    items = fields.List(fields.Nested(TransactionSchema), dump_only=True)
    pagination = fields.Dict(dump_only=True)

