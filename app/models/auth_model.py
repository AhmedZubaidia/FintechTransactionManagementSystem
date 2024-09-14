import enum
from sqlalchemy import Enum as SQLAlchemyEnum


# Define Enum for role
class UserRole(enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"


# Define Enum for user types
class UserType(enum.Enum):
    CLIENT = "Client"
    ADMIN = "Admin"


from datetime import datetime
from app import db
from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SQLAlchemyEnum


# Assuming UserRole and UserType enums are imported here

class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Role with Enum constraint: either "admin" or "client"
    role = db.Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.CLIENT, server_default="client")
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # User type as Enum
    user_type = db.Column(SQLAlchemyEnum(UserType), nullable=False, default=UserType.CLIENT)

    last_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)

    # Relationship with User model
    user = db.relationship('User', backref=db.backref('auth', lazy=True))

    def __repr__(self):
        return f'<Auth {self.username} ({self.role.value})>'
