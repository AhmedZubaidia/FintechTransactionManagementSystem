from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_babel import Babel  # Add Flask-Babel import
from config import Config

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    babel.init_app(app)

    # Import models so they are registered properly with SQLAlchemy
    from app.models.auth_model import Auth
    from app.models.user_model import User  # Import User model here
    from app.models.transaction_model import TransactionModel  # Import TransactionModel as well

    # Register blueprints
    from app.routes.user.auth.apis import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.routes.user.profile.apis import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api')

    from app.routes.transactions.client.apis import bp as transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')

    return app
