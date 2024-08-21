# app/models/transaction.py
from datetime import datetime

from app import db
from app.models.base_model import BaseModel


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Transaction {self.amount} - {self.category}>'


# Late import to avoid circular dependency
from app.models.user import User

Transaction.user = db.relationship('User', back_populates='transactions')
