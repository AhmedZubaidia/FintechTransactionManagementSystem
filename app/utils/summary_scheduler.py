from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.transaction_model import TransactionModel
from app.models.user_model import User
from datetime import datetime, timedelta
from app.third_parties.telegram.send_message import send_message


def send_periodic_summary_for_user(app):
    with app.app_context():
        # Get the time 24 hours ago
        since = datetime.utcnow() - timedelta(days=1)

        # Query all users
        users = User.query.all()

        for user in users:
            # Query transactions for the specific user made in the last 24 hours
            transactions = TransactionModel.query.filter(
                TransactionModel.user_id == user.id,
                TransactionModel.timestamp >= since
            ).all()

            # Initialize credit and debit totals
            total_credit = 0
            total_debit = 0

            for transaction in transactions:
                # Ensure transaction_type is evaluated properly
                if transaction.transaction_type == 'credit':
                    total_credit += transaction.amount
                elif transaction.transaction_type == 'debit':
                    total_debit += transaction.amount

            # Prepare the balance and summary
            balance = total_credit - total_debit
            message = (f"Transaction Summary for {user.username} (Last 24 hours):\n"
                       f"Total Credit: {total_credit}\n"
                       f"Total Debit: {total_debit}\n"
                       f"Balance: {balance}\n"
                       f"Transactions Count: {len(transactions)}")

            # Send the summary to the user's chat via Telegram
            chat_id = current_app.config['TELEGRAM_CHAT_ID']  # Adjust to fetch user's Telegram chat ID if available
            send_message(message, chat_id)


def setup_user_scheduler(app):
    scheduler = BackgroundScheduler()

    # Pass the `app` instance to the scheduled job
    scheduler.add_job(func=send_periodic_summary_for_user, trigger="interval", minutes=1, args=[app])
    scheduler.start()

