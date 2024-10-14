from datetime import datetime
from app import db
from flask_jwt_extended import decode_token
from app.models.base_model import BaseModel  # Import BaseModel
import enum
from sqlalchemy import Enum as SQLAlchemyEnum


# Enum for gender
class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# Enum for preferred language
class PreferredLanguage(enum.Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    ARABIC = "ar"


# Enum for currency
class Currency(enum.Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"


class User(BaseModel):  # Inherit from BaseModel
    __tablename__ = 'user'

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Additional fields specific to User
    full_name = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    # Gender attribute using Enum
    gender = db.Column(SQLAlchemyEnum(Gender), nullable=True, default=Gender.MALE)

    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)

    session_id = db.Column(db.String(255), nullable=True)
    device_id = db.Column(db.String(255), nullable=True)

    # Preferred language using Enum
    preferred_language = db.Column(SQLAlchemyEnum(PreferredLanguage), nullable=True, default=PreferredLanguage.ENGLISH)

    # Currency using Enum
    currency = db.Column(SQLAlchemyEnum(Currency), nullable=True, default=Currency.USD)

    # Soft delete field
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    # Roles attribute (assuming roles are still used)
    roles = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User {self.username}, Gender: {self.gender.value}, Language: {self.preferred_language.value}, Currency: {self.currency.value}>'

    # Define the relationship between User and TransactionModel lazily to avoid circular import
    @property
    def transactions(self):
        from app.models.transaction_model import TransactionModel  # Delayed import
        return db.relationship('TransactionModel', back_populates='user', lazy="dynamic")

    # Soft delete method
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    # Restore a soft-deleted user
    def restore(self):
        self.deleted_at = None

    # Check if user is soft deleted
    @property
    def is_deleted(self):
        return self.deleted_at is not None
