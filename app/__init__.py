from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from config import Config
from app.scheduler import scheduler
from app.cronjobs import setup_system_wide_scheduler
import logging

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    babel.init_app(app)

    # Import models to register them with SQLAlchemy
    from app.models.auth_model import Auth
    from app.models.user_model import User
    from app.models.transaction_model import TransactionModel

    # Register blueprints for routes
    from app.routes.user.auth.apis import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.routes.user.profile.apis import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api')

    from app.routes.transactions.client.apis import bp as client_transaction_bp
    app.register_blueprint(client_transaction_bp, url_prefix='/api/transactions/client')

    from app.routes.transactions.admin.apis import bp as admin_transaction_bp
    app.register_blueprint(admin_transaction_bp, url_prefix='/api/transactions/admin')

    # Start the scheduler
    setup_scheduler(app)

    return app


def setup_scheduler(app):
    with app.app_context():
        scheduler.start()

    setup_system_wide_scheduler(app)  # Setup cron jobs
