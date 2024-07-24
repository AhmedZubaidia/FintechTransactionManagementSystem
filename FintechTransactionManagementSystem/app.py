from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myLearningApp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TELEGRAM_BOT_TOKEN'] = "7270283184:AAHZuYyjsT33FY8oBqM0ccRbT5-mYTzLb7Q"

    db.init_app(app)
    migrate = Migrate(app, db)

    from FintechTransactionManagementSystem.routes import register_routes
    register_routes(app, db)

    return app
