import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.logic.transaction.client.list_my_transactions import execute
from flask import Flask

# Mock class to simulate transactions for a user
class MockTransaction:
    def __init__(self, id, amount, transaction_type, timestamp):
        self.id = id
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = timestamp


class MockQuery:
    def filter_by(self, user_id):
        # Return an object with an .all() method
        class QueryWithAll:
            def paginate(self, page, per_page, error_out=False):
                # Simulate transactions for user_id 1
                if user_id == 1:
                    items = [
                        MockTransaction(id=1, amount=100, transaction_type=MagicMock(value='credit'), timestamp=datetime(2024, 10, 1, 10, 0, 0)),
                        MockTransaction(id=2, amount=50, transaction_type=MagicMock(value='debit'), timestamp=datetime(2024, 10, 2, 12, 0, 0))
                    ]
                    total = len(items)
                    return MagicMock(items=items, total=total)
                # Simulate no transactions for user_id 999
                if user_id == 999:
                    items = []
                    total = len(items)
                    return MagicMock(items=items, total=total)
                return None

        return QueryWithAll()


# Test for successfully generating a transaction report for a client with transactions
@patch('app.logic.transaction.client.list_my_transactions.TransactionModel', new=MagicMock())
def test_execute_list_my_transactions_success():
    mock_query = MockQuery()
    MagicMock.query = mock_query  # Attach mock query to TransactionModel

    # Call the execute function for a client with transactions
    paginated_transactions = execute(page=1, per_page=10, user_id_token=1)

    # Assertions for the report
    assert paginated_transactions.total == 2
    assert len(paginated_transactions.items) == 2
    assert paginated_transactions.items[0].amount == 100
    assert paginated_transactions.items[1].amount == 50
    assert paginated_transactions.items[0].transaction_type.value == 'credit'


# Test for generating a transaction report for a client with no transactions
@patch('app.logic.transaction.client.list_my_transactions.TransactionModel', new=MagicMock())
def test_execute_list_my_transactions_no_transactions():
    app = Flask(__name__)
    with app.app_context():
        mock_query = MockQuery()
        MagicMock.query = mock_query  # Attach mock query to TransactionModel

        # Call the execute function for a client with no transactions
        paginated_transactions = execute(page=1, per_page=10, user_id_token=999)

        # Assertions for the report
        assert paginated_transactions.total == 0
        assert len(paginated_transactions.items) == 0
