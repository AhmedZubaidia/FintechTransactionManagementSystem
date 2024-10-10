from marshmallow import Schema, fields, validate


class PaginatedSchema(Schema):
    # Fields for pagination input validation
    page = fields.Int(load_only=True, load_default=1)
    per_page = fields.Int(load_only=True, load_default=10, validate=[validate.Range(min=1, max=100)])

    # items will be populated dynamically with a nested schema
    items = fields.List(fields.Nested(lambda: None), dump_only=True)  # We'll replace None with the dynamic schema

    # Metadata for pagination (e.g., total items, total pages, next/prev page)
    pagination = fields.Dict(dump_only=True)

    user_id = fields.Int(load_only=True)
    user_id_token = fields.Int(load_only=True)

    def __init__(self, item_schema, *args, **kwargs):
        # Dynamically set the items field with the passed schema
        super().__init__(*args, **kwargs)
        self.fields['items'] = fields.List(fields.Nested(item_schema), dump_only=True)

    @staticmethod
    def generate_pagination_metadata(page, per_page, total_items):

        total_pages = (total_items + per_page - 1) // per_page  # Calculate total pages
        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        return {
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'next_page': next_page,
            'previous_page': previous_page,
            'has_next': next_page is not None,
            'has_previous': previous_page is not None
        }
