from app.models.usertransaction import UserTransaction


def execute(user_id):
    transactions = UserTransaction.query.filter_by(user_id=user_id).all()

    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expenses

    categories = {}
    for transaction in transactions:
        if transaction.category not in categories:
            categories[transaction.category] = 0
        categories[transaction.category] += transaction.amount

    report = {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'categories': categories
    }
    return report
