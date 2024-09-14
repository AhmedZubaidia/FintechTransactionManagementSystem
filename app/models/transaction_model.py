from datetime import datetime
from app import db
from app.models.base_model import BaseModel  # Assuming you're extending a BaseModel class
import enum
from sqlalchemy import Enum as SQLAlchemyEnum


# Enum for transaction type
class TransactionType(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"


# Enum for transaction category (example categories)
class TransactionCategory(enum.Enum):
    SALARY = "salary"
    PURCHASE = "purchase"
    TRANSFER = "transfer"


class TransactionModel(BaseModel):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(SQLAlchemyEnum(TransactionCategory), nullable=False)  # Use Enum for category
    description = db.Column(db.String(200), nullable=True)
    type = db.Column(SQLAlchemyEnum(TransactionType), nullable=False)  # Use Enum for transaction type (credit/debit)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    session_id = db.Column(db.String(255), nullable=True)
    device_id = db.Column(db.String(255), nullable=True)

    # Link to the User model using a delayed import to avoid circular import
    @property
    def user(self):
        from app.models.user_model import User
        return db.relationship('User', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.amount} - {self.category.value}>'
