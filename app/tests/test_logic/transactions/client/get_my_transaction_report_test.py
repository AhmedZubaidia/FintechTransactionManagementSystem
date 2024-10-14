import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.logic.transaction.client.list_my_transactions import execute

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
            def all(self):
                # Simulate transactions for user_id 1
                if user_id == 1:
                    return [
                        MockTransaction(id=1, amount=100, transaction_type=MagicMock(value='credit'), timestamp=datetime(2024, 10, 1, 10, 0, 0)),
                        MockTransaction(id=2, amount=50, transaction_type=MagicMock(value='debit'), timestamp=datetime(2024, 10, 2, 12, 0, 0))
                    ]
                # Simulate no transactions for user_id 999
                if user_id == 999:
                    return []
                return None

        return QueryWithAll()


# Test for successfully generating a transaction report for a client with transactions
@patch('app.logic.transaction.client.list_my_transactions.TransactionModel', new=MagicMock())
def test_execute_generate_transaction_report_success():
    mock_query = MockQuery()
    MagicMock.query = mock_query  # Attach mock query to TransactionModel

    # Call the execute function for a client with transactions
    result = execute(page=1, per_page=10, user_id_token=1)

    # Assertions for the report
    assert result['user']['id'] == 1
    assert result['credit'] == 100
    assert result['debit'] == 50
    assert result['balance'] == 50
    assert result['last_transaction_datetime'] == '2024-10-02 12:00:00'


# Test for generating a transaction report for a client with no transactions
@patch('app.logic.transaction.client.list_my_transactions.TransactionModel', new=MagicMock())
@patch('flask.current_app.app_context', new=MagicMock())
def test_execute_generate_transaction_report_no_transactions():
    mock_query = MockQuery()
    MagicMock.query = mock_query  # Attach mock query to TransactionModel

    # Call the execute function for a client with no transactions
    result = execute(page=1, per_page=10, user_id_token=999)

    # Assertions for the report
    assert result['user']['id'] == 999
    assert result['credit'] == 0
    assert result['debit'] == 0
    assert result['balance'] == 0
    assert result['last_transaction_datetime'] is None