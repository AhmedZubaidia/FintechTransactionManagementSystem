from datetime import datetime
from app import db
from flask_jwt_extended import get_jwt_identity


class BaseModel(db.Model):
    __abstract__ = True  # This makes sure BaseModel itself doesn't create a table

    created_by = db.Column(db.Integer, nullable=True)
    modified_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self, current_user_id=None):
        if current_user_id is None:
            try:
                current_user_id = get_jwt_identity()
            except Exception as e:
                raise RuntimeError("JWT identity not available. Ensure this method is called in a request context.")

        if not self.id:  # If the record is new
            self.created_by = current_user_id
        self.modified_by = current_user_id

        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
