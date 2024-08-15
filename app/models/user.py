# app/models/user.py
from app import db
from app.models.base_model import BaseModel


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# Late import to avoid circular dependency
from app.models.transaction import Transaction

User.transactions = db.relationship('Transaction', back_populates='user', lazy=True)
