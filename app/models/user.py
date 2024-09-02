from app import db
from app.models.base_model import BaseModel


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    session_id = db.Column(db.String(255), nullable=True)
    device_id = db.Column(db.String(255), nullable=True)
    preferred_language = db.Column(db.String(10), nullable=True)
    currency = db.Column(db.String(10), nullable=True)

    # Add the roles attribute
    roles = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'


# The relationship is added after the UserTransaction class is defined
from app.models.usertransaction import UserTransaction

User.transactions = db.relationship('UserTransaction', back_populates='user', lazy=True)
