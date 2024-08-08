from app.models.transaction import Transaction

def execute():
    transactions = Transaction.query.all()
    transactions_list = [{'id': t.id, 'user_id': t.user_id, 'amount': t.amount, 'category': t.category, 'description': t.description, 'timestamp': t.timestamp} for t in transactions]
    return transactions_list, 200



def execute_by_id(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        return {'message': 'Transaction not found'}, 404
    return transaction, 200
