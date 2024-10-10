from datetime import datetime
from app import db
from app.models.base_model import BaseModel
import enum
from sqlalchemy import Enum as SQLAlchemyEnum


# Enum for transaction type
class TransactionType(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"


# Enum for transaction category
class TransactionCategory(enum.Enum):
    SALARY = "salary"
    PURCHASE = "purchase"
    TRANSFER = "transfer"


class TransactionModel(BaseModel):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(SQLAlchemyEnum(TransactionCategory), nullable=False)  # Enum for category
    description = db.Column(db.String(200), nullable=True)
    transaction_type = db.Column(SQLAlchemyEnum(TransactionType), nullable=False)  # Enum for transaction type (credit/debit)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    session_id = db.Column(db.String(255), nullable=True)
    device_id = db.Column(db.String(255), nullable=True)

    # Soft delete field
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    # Relationship to the User model (delayed import)
    @property
    def user(self):
        from app.models.user_model import User
        return db.relationship('User', back_populates='transactions')

    # Convert the transaction object to a dictionary with enum values
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category.value,  # Convert Enum to its value (e.g., 'salary')
            "description": self.description,
            "transaction_type": self.transaction_type.value,  # Convert Enum to its value (e.g., 'credit')
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "device_id": self.device_id,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }

    def __repr__(self):
        return f'<Transaction {self.amount} - {self.category.value}>'

    # Soft delete method
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    # Restore a soft-deleted transaction
    def restore(self):
        self.deleted_at = None

    # Check if transaction is soft deleted
    @property
    def is_deleted(self):
        return self.deleted_at is not None
