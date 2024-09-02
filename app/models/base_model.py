from datetime import datetime

from flask import has_request_context
from flask_jwt_extended import get_jwt_identity, get_jwt, decode_token

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    created_by = db.Column(db.String(255), nullable=True)
    modified_by = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self):
        self.device_id = None
        self.session_id = None

    def save(self, jwt_token=None, session_id=None, device_id=None):

        if jwt_token:
            # Extract the 'sub' part from the JWT
            encrypted_user_id = jwt_token.split('.')[1]
            if not self.id:  # if the record is new
                self.created_by = encrypted_user_id
            self.modified_by = encrypted_user_id

        self.session_id = session_id
        self.device_id = device_id
        self.modified_at = datetime.utcnow()

        db.session.add(self)
        db.session.commit()
