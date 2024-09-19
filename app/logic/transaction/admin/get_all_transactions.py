from app.models.transaction_model import TransactionModel


def execute(page, per_page):

    transactions_query = TransactionModel.query.paginate(page=page, per_page=per_page, error_out=False)

    transactions = [transaction.to_dict() for transaction in transactions_query.items]

    return transactions, transactions_query.total
