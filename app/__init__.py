from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_babel import Babel  # Add Flask-Babel import
from config import Config

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()  # Initialize Flask-Babel


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    babel.init_app(app)  # Initialize Flask-Babel with the app

    from app.routes.user.auth.apis import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    from app.routes.user.profile.apis import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api/profile')

    from app.routes.transactions.apis import bp as transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')

    return app
