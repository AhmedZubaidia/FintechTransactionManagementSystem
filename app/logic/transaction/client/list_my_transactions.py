from app.models.transaction_model import TransactionModel


def execute(page, per_page, user_id_token=None):
    transactions_query = TransactionModel.query.filter_by(user_id=user_id_token)

    # Use pagination correctly (only pass page and per_page)
    paginated_transactions = transactions_query.paginate(page=page, per_page=per_page, error_out=False)

    return paginated_transactions
