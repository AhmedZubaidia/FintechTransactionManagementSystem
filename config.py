class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///myLearningApp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'

    # Telegram Configuration
    TELEGRAM_TOKEN = '7270283184:AAHZuYyjsT33FY8oBqM0ccRbT5-mYTzLb7Q'
    TELEGRAM_CHAT_ID = '6526202532'
