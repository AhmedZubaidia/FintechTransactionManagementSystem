import pytest
from unittest.mock import patch, MagicMock
from app.logic.transaction.client.get_transaction_by_id import execute
from app.utils.exceptions import appNotFoundError, appForbiddenError


# Mock class to simulate a transaction
class MockTransaction:
    def __init__(self, id, user_id, amount, transaction_type):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type
        }


# Test for successfully fetching a transaction by ID
@patch('app.logic.transaction.client.get_transaction_by_id.TransactionModel')
def test_execute_get_transaction_by_id_success(MockTransactionModel):
    mock_transaction = MockTransaction(id=1, user_id=1, amount=100, transaction_type='credit')
    MockTransactionModel.query.get.return_value = mock_transaction  # Mock the query to return the transaction

    # Call the execute function
    result = execute(id=1, user_id_token=1)

    # Assertions for the transaction
    assert result['id'] == 1
    assert result['user_id'] == 1
    assert result['amount'] == 100
    assert result['transaction_type'] == 'credit'


# Test for transaction not found
@patch('app.logic.transaction.client.get_transaction_by_id.TransactionModel')
def test_execute_get_transaction_by_id_not_found(MockTransactionModel):
    MockTransactionModel.query.get.return_value = None  # Mock the query to return None

    # Call the execute function and expect an exception
    with pytest.raises(appNotFoundError) as excinfo:
        execute(id=999, user_id_token=1)

    # Assert the correct error message
    assert str(excinfo.value) == "Transaction with ID 999 not found"


# Test for forbidden access to transaction
@patch('app.logic.transaction.client.get_transaction_by_id.TransactionModel')
def test_execute_get_transaction_by_id_forbidden(MockTransactionModel):
    mock_transaction = MockTransaction(id=1, user_id=2, amount=100, transaction_type='credit')
    MockTransactionModel.query.get.return_value = mock_transaction  # Mock the query to return a transaction belonging to another user

    # Call the execute function and expect an exception
    with pytest.raises(appForbiddenError) as excinfo:
        execute(id=1, user_id_token=1)

    # Assert the correct error message
    assert str(excinfo.value) == "No Transaction with ID {transaction_id} found for the current user"
