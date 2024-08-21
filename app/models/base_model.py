from flask import has_request_context
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # This makes sure BaseModel itself doesn't create a table

    # Store the user ID instead of the JWT token
    created_by = db.Column(db.Integer, nullable=True)  # Assuming user IDs are integers
    modified_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self, current_user_id=None):
        if current_user_id is None:
            if has_request_context():
                try:
                    current_user_id = get_jwt_identity()  # Retrieve the user ID directly
                except Exception as e:
                    raise RuntimeError("JWT identity not available. Ensure this method is called in a request context.")
            else:
                raise RuntimeError("Request context is required to automatically determine current_user_id.")

        if not self.id:  # If the record is new
            self.created_by = current_user_id
        self.modified_by = current_user_id

        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
