import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.logic.transaction.admin.delete_transaction import execute


# Mock class to simulate a transaction
class MockTransaction:
    def __init__(self, id, user_id, is_deleted=False):
        self.id = id
        self.user_id = user_id
        self.is_deleted = is_deleted

    def save(self, user_id_token):
        pass

    def soft_delete(self):
        self.is_deleted = True


# Mock class for simulating the database session
class MockDbSession:
    def commit(self):
        pass


# Test for successfully deleting a transaction
@patch('app.logic.transaction.admin.delete_transaction.TransactionModel', new=MagicMock())
@patch('app.logic.transaction.admin.delete_transaction.db', new=MagicMock(session=MockDbSession()))
def test_execute_delete_transaction_success():
    mock_transaction = MockTransaction(id=1, user_id=1)
    mock_transaction_model = MagicMock()
    mock_transaction_model.query.get.return_value = mock_transaction

    # Patch the TransactionModel.query to return the mock transaction
    with patch('app.logic.transaction.admin.delete_transaction.TransactionModel', mock_transaction_model):
        # Call the execute function
        result = execute(id=1, user_id_token=1)

        # Assertions
        assert result['message'] == "Transaction soft deleted successfully"
        assert mock_transaction.is_deleted is True


# Test for transaction not found or already deleted
@patch('app.logic.transaction.admin.delete_transaction.TransactionModel', new=MagicMock())
def test_execute_delete_transaction_not_found():
    mock_transaction_model = MagicMock()
    mock_transaction_model.query.get.return_value = None  # Simulate transaction not found

    # Patch the TransactionModel.query to return None
    with patch('app.logic.transaction.admin.delete_transaction.TransactionModel', mock_transaction_model):
        # Call the execute function
        result = execute(id=999, user_id_token=1)

        # Assertions
        assert 'error' in result
        assert result['error'] == "Transaction not found or be deleted or not belong to the current user"


