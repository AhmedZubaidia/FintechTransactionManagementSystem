from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    cors = CORS(app, origins="*")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myLearningApp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TELEGRAM_BOT_TOKEN'] = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Change this in production

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    from FintechTransactionManagementSystem.routes import register_routes
    register_routes(app, db)

    return app
