from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app import scheduler
from app.models.auth_model import Auth
from app.models.user_model import User
from app.third_parties.telegram.send_login_notification import send_login_notification
from app.utils.exceptions import appLoginError

from flask import current_app
from app import db
from app.models.transaction_model import TransactionModel
from app.third_parties.telegram.send_message import send_message
from datetime import datetime, timedelta


def execute(email, password):
    user = User.query.filter_by(email=email).first()
    auth = Auth.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        chat_id = current_app.config['TELEGRAM_CHAT_ID']
        send_login_notification(user.username, chat_id)

        additional_claims = {
            "username": user.username,
            "email": user.email,
            "role": auth.role.value,
        }

        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

        # Schedule the periodic summary job for this user
        setup_user_scheduler(user.id, current_app)

        return dict(message='Login successful', access_token=access_token)

    raise appLoginError('Invalid email or password')


def send_periodic_summary_for_user(user_id, app):
    # Use the application context explicitly
    with app.app_context():
        since = datetime.utcnow() - timedelta(days=1)
        transactions = TransactionModel.query.filter(
            TransactionModel.user_id == user_id,
            TransactionModel.timestamp >= since
        ).all()

        if transactions:
            total_credit = sum(tx.amount for tx in transactions if tx.transaction_type.value == 'credit')
            total_debit = sum(tx.amount for tx in transactions if tx.transaction_type.value == 'debit')
            balance = total_credit - total_debit

            message = (f"Transaction Summary for User ID {user_id} (Last 24 hours):\n"
                       f"Total Credit: {total_credit}\n"
                       f"Total Debit: {total_debit}\n"
                       f"Balance: {balance}\n"
                       f"Transactions Count: {len(transactions)}")

            chat_id = current_app.config['TELEGRAM_CHAT_ID']
            send_message(message, chat_id)


def setup_user_scheduler(user_id, app):
    job_id = f"user_summary_{user_id}"

    # Check if the job already exists to avoid adding duplicate jobs
    if scheduler.get_job(job_id):
        return

    # Pass the app's current object to ensure context binding
    app_context = app._get_current_object()

    # Schedule the job to run every minute
    scheduler.add_job(
        func=send_periodic_summary_for_user,
        trigger="interval",
        minutes=1,
        args=[user_id, app_context],  # Pass the app's current object
        id=job_id
    )
