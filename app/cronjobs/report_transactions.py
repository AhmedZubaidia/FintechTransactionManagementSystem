from datetime import datetime, timedelta
from flask import current_app
from app.third_parties.telegram.send_message import send_message


def send_periodic_summary_for_all_users(app):
    # Import `db` and models inside the function to avoid circular imports
    from app.models.transaction_model import TransactionModel
    from app.models.user_model import User

    # Use the application context explicitly
    with app.app_context():
        since = datetime.utcnow() - timedelta(days=1)

        # Query all users in the system
        users = User.query.all()

        for user in users:
            transactions = TransactionModel.query.filter(
                TransactionModel.user_id == user.id,
                TransactionModel.timestamp >= since
            ).all()

            if transactions:
                total_credit = sum(tx.amount for tx in transactions if tx.transaction_type.value == 'credit')
                total_debit = sum(tx.amount for tx in transactions if tx.transaction_type.value == 'debit')
                balance = total_credit - total_debit

                message = (f"Transaction Summary for User ID {user.id} ({user.username}) (Last 24 hours):\n"
                           f"Total Credit: {total_credit}\n"
                           f"Total Debit: {total_debit}\n"
                           f"Balance: {balance}\n"
                           f"Transactions Count: {len(transactions)}")

                chat_id = current_app.config['TELEGRAM_CHAT_ID']
                send_message(message, chat_id)
