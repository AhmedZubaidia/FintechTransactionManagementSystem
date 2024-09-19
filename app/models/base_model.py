from datetime import datetime
from app import db


class BaseModel(db.Model):
    __abstract__ = True  # This prevents the creation of a table for this class

    # Common fields for all models
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(255), nullable=True)
    modified_by = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self, user_id, is_new=False):
        # Set created_by only when the record is new
        if is_new:
            self.created_by = str(user_id)
            self.created_at = datetime.utcnow()
        else:
            self.modified_by = str(user_id)
            self.modified_at = datetime.utcnow()

        # Add the model instance to the session and commit
        db.session.add(self)
        db.session.commit()

    def delete(self, user_id):
        print(f"Record with ID {self.id} is being deleted by user {user_id}")
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, created_by={self.created_by}, modified_by={self.modified_by}>'
