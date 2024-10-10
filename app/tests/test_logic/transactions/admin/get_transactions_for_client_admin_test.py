import pytest
from unittest.mock import patch, MagicMock
from app.logic.transaction.admin.get_transactions_for_client import execute
from app.utils.exceptions import appNotFoundError


# Mock class to simulate transactions for a user
class MockTransaction:
    def __init__(self, id, amount, description):
        self.id = id
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description
        }


class MockQuery:
    def filter_by(self, user_id):
        # Return an object with a .paginate() method
        class QueryWithPaginate:
            def paginate(self, page, per_page, error_out):
                # Simulate transactions for user_id 1
                if user_id == 1:
                    items = [MockTransaction(id=1, amount=100, description='Salary Payment'),
                             MockTransaction(id=2, amount=200, description='Purchase')]
                    mock_paginate = MagicMock()
                    mock_paginate.items = [t.to_dict() for t in items]
                    mock_paginate.total = len(items)
                    return mock_paginate
                # Simulate no transactions for user_id 999
                if user_id == 999:
                    mock_paginate = MagicMock()
                    mock_paginate.items = []
                    mock_paginate.total = 0
                    return mock_paginate
                return None

        return QueryWithPaginate()


# Test for successfully retrieving transactions for a client
@patch('app.logic.transaction.admin.get_transactions_for_client.TransactionModel', new=MagicMock())
def test_execute_get_transactions_for_client_success():
    mock_query = MockQuery()
    mock_transaction_model = MagicMock()
    mock_transaction_model.query = mock_query  # Attach mock query to TransactionModel

    with patch('app.logic.transaction.admin.get_transactions_for_client.TransactionModel', mock_transaction_model):
        # Call the execute function for a client with transactions
        result = execute(user_id=1, page=1, per_page=10)

        transactions = result.items

        # Assertions for the transactions
        assert len(transactions) == 2
        assert transactions[0]['description'] == 'Salary Payment'
        assert transactions[1]['description'] == 'Purchase'


# Test for client with no transactions
@patch('app.logic.transaction.admin.get_transactions_for_client.TransactionModel', new=MagicMock())
def test_execute_get_transactions_for_client_not_found():
    mock_query = MockQuery()
    mock_transaction_model = MagicMock()
    mock_transaction_model.query = mock_query  # Attach mock query to TransactionModel

    with patch('app.logic.transaction.admin.get_transactions_for_client.TransactionModel', mock_transaction_model):
        # Expect an exception for a client with no transactions
        with pytest.raises(appNotFoundError) as excinfo:
            execute(user_id=999, page=1, per_page=10)

        # Assert the correct error message
        assert str(excinfo.value) == "User with ID 999 has no transactions"