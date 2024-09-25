from app.models.transaction_model import TransactionModel


def execute(page, per_page):

    transactions = TransactionModel.query.paginate(page=page, per_page=per_page, error_out=False)

    return transactions
