import pytest
from unittest.mock import patch, MagicMock
from app.logic.transaction.admin.get_all_transactions import execute


# Mock class to simulate paginated transactions
class MockTransaction:
    def __init__(self, id, amount, description):
        self.id = id
        self.amount = amount
        self.description = description


class MockPaginate:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total


class MockQuery:
    def paginate(self, page, per_page, error_out):
        return MockPaginate(
            items=[MockTransaction(id=1, amount=100, description='Salary Payment'),
                   MockTransaction(id=2, amount=200, description='Purchase')],
            page=page,
            per_page=per_page,
            total=2
        )


# Mock the TransactionModel and paginate behavior
@patch('app.logic.transaction.admin.get_all_transactions.TransactionModel', new=MagicMock())
def test_execute_get_all_transactions_success():
    mock_query = MockQuery()
    MagicMock.query = mock_query  # Attach mock query to TransactionModel

    # Test data
    page = 1
    per_page = 10

    # Call the execute function
    result = execute(page, per_page)

    # Assertions for the pagination object
    assert result.page == 1
    assert result.per_page == 10
    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].description == 'Salary Payment'
    assert result.items[1].description == 'Purchase'
