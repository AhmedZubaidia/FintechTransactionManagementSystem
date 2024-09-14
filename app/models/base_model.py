from datetime import datetime
from app import db
from flask_jwt_extended import decode_token  # Import for decoding the JWT token


class BaseModel(db.Model):
    __abstract__ = True  # This prevents the creation of a table for this class

    # Common fields for all models
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(255), nullable=True)
    modified_by = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def extract_user_id_from_token(self, jwt_token):
        # Ensure the token is provided and well-formed
        if not jwt_token or len(jwt_token.split('.')) != 3:
            raise ValueError("Invalid JWT token: not enough segments")

        decoded_token = decode_token(jwt_token)  # Decode the JWT token
        return decoded_token.get('user_id')  # Extract the user ID from the token

    def save(self, jwt_token=None, session_id=None, device_id=None, is_new=False):

        if jwt_token:
            # Extract user ID from the JWT token
            user_id = self.extract_user_id_from_token(jwt_token)

            # Set created_by only when the record is new
            if is_new:
                self.created_by = str(user_id)
                self.created_at = datetime.utcnow()  # Ensuring created_at is only set once during creation

            # Set modified_by and always update modified_at
            self.modified_by = str(user_id)

        # Update modified_at for every save
        self.modified_at = datetime.utcnow()

        # Save the changes to the database
        db.session.add(self)
        db.session.commit()

    def delete(self, jwt_token=None):

        if jwt_token:

            user_id = self.extract_user_id_from_token(jwt_token)
            print(f"Record with ID {self.id} is being deleted by user {user_id}")

        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, created_by={self.created_by}, modified_by={self.modified_by}>'
