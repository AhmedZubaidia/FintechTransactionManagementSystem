from app.models.transaction_model import TransactionModel


def execute(client_id):
    transactions = TransactionModel.query.filter_by(user_id=client_id).all()

    credit_total = sum(t.amount for t in transactions if t.type == "credit")
    debit_total = sum(t.amount for t in transactions if t.type == "debit")
    balance = credit_total - debit_total

    last_transaction = max(transactions, key=lambda t: t.timestamp, default=None)

    report = {
        "user": {
            "id": client_id,
        },
        "credit": credit_total,
        "debit": debit_total,
        "balance": balance,
        "last_transaction_datetime": last_transaction.timestamp if last_transaction else None
    }

    return report, 200
