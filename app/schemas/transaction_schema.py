from marshmallow import Schema, fields, validate
from app.models.transaction_model import TransactionCategory, TransactionType
from marshmallow import fields

# Custom field to handle enum serialization/deserialization
from marshmallow import fields, ValidationError


# Custom field to handle enum serialization/deserialization
class EnumField(fields.Field):
    default_error_messages = {
        "invalid_value": "Invalid value for enum {enum_name}: {input_value}."
    }

    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, self.enum):
            return value.name  # Serialize enum as its name
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        # If value is a string, convert to uppercase for case-insensitive matching
        if isinstance(value, str):
            value = value.upper()

        # Ensure value is either string or enum before returning
        if isinstance(value, self.enum):
            return value  # Return if it's already an enum

        # Raise ValidationError if the value is invalid
        try:
            return self.enum[value]  # Attempt to match string to enum
        except KeyError:
            # Raise a detailed ValidationError explaining the invalid input
            raise ValidationError(f"Invalid value '{value}' for enum {self.enum.__name__}. "
                                  f"Valid values are: {[member.name for member in self.enum]}")


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)  # If user_id is required during input
    user_id_token = fields.Int(required=True)  # If user_id is set

    amount = fields.Float(required=True)  # Remove dump_only to allow for deserialization

    # Use custom EnumField to serialize/deserialize enums
    category = EnumField(TransactionCategory, required=True)
    transaction_type = EnumField(TransactionType, required=True)

    description = fields.Str(validate=[validate.Length(max=200)])
    timestamp = fields.DateTime(dump_only=True)


class reportSchema(Schema):
    user_id = fields.Int()
    user_id_token = fields.Int()


class TransactionDeleteSchema(Schema):
    id = fields.Int(required=True)
    user_id_token = fields.Int(required=True)


class TransactionClientSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id_token = fields.Int(required=True)  # If user_id is set
    amount = fields.Float(required=True)  # Remove dump_only to allow for deserialization
    category = EnumField(TransactionCategory, required=True)
    transaction_type = EnumField(TransactionType, required=True)
    description = fields.Str(validate=[validate.Length(max=200)])
    timestamp = fields.DateTime(dump_only=True)


class TransactionOutputSchema(Schema):
    id = fields.Int(load_only=True)
    user_id = fields.Int()  # If user_id is required during input
    user_id_token = fields.Int()  # If user_id is set

    amount = fields.Float(dump_only=True)  # Remove dump_only to allow for deserialization

    # Use custom EnumField to serialize/deserialize enums
    category = EnumField(TransactionCategory, dump_only=True)
    transaction_type = EnumField(TransactionType, dump_only=True)

    description = fields.Str(validate=[validate.Length(max=200)])
    timestamp = fields.DateTime(dump_only=True)
