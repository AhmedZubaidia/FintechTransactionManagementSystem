import pytest
from unittest.mock import patch, MagicMock
from app.logic.transaction.client.create_transaction import execute
from app.utils.exceptions import appNotFoundError
from app.models.transaction_model import TransactionCategory, TransactionType


# Mock classes to simulate User and TransactionModel
class MockUser:
    def __init__(self, id, is_deleted=False, username='test_user'):
        self.id = id
        self.is_deleted = is_deleted
        self.username = username


class MockTransactionModel:
    def __init__(self, user_id, amount, category, transaction_type, description):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.description = description

    def save(self, user_id_token, is_new=False):
        pass

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'transaction_type': self.transaction_type,
            'description': self.description
        }


class MockQuery:
    def get(self, user_id):
        if user_id == 1:
            return MockUser(id=user_id)  # Simulate user found
        return None  # Simulate user not found


class MockDbSession:
    def add(self, obj):
        pass

    def commit(self):
        pass


class MockDb:
    session = MockDbSession()  # Add a session object


# Test for successfully creating a transaction
@patch('app.logic.transaction.client.create_transaction.User', new=MockUser)
@patch('app.logic.transaction.client.create_transaction.TransactionModel', new=MockTransactionModel)
@patch('app.logic.transaction.client.create_transaction.db', new=MockDb)
@patch('app.logic.transaction.client.create_transaction.current_app', new=MagicMock(config={'TELEGRAM_CHAT_ID': '12345'}))
@patch('app.logic.transaction.client.create_transaction.send_message', new=MagicMock())
def test_execute_create_transaction_success():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to MockUser class

    # Test data
    data = {
        'amount': 100,
        'category': TransactionCategory.SALARY,
        'transaction_type': TransactionType.CREDIT,
        'description': 'Dinner payment',
        'user_id_token': 1
    }

    # Call the execute function
    result = execute(**data)

    # Assertions
    assert result['user_id'] == 1
    assert result['amount'] == 100
    assert result['category'] == TransactionCategory.SALARY.value
    assert result['transaction_type'] == TransactionType.CREDIT.value
    assert result['description'] == 'Dinner payment'


# Test for user not found
@patch('app.logic.transaction.client.create_transaction.User', new=MockUser)
@patch('app.logic.transaction.client.create_transaction.db', new=MockDb)
@patch('app.logic.transaction.client.create_transaction.current_app', new=MagicMock(config={'TELEGRAM_CHAT_ID': '12345'}))
def test_execute_create_transaction_user_not_found():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to MockUser class

    # Test data
    data = {
        'amount': 100,
        'category': TransactionCategory.SALARY,
        'transaction_type': TransactionType.CREDIT,
        'description': 'Dinner payment',
        'user_id_token': 999
    }

    # Call the execute function and expect an exception
    with pytest.raises(appNotFoundError) as excinfo:
        execute(**data)

    # Assert the correct error message
    assert str(excinfo.value) == "User with ID 999 not found"


# Test for invalid category or transaction type
@patch('app.logic.transaction.client.create_transaction.User', new=MockUser)
@patch('app.logic.transaction.client.create_transaction.db', new=MockDb)
@patch('app.logic.transaction.client.create_transaction.current_app', new=MagicMock(config={'TELEGRAM_CHAT_ID': '12345'}))
def test_execute_create_transaction_invalid_category_or_type():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to MockUser class

    # Test data with an invalid category
    data_invalid_category = {
        'amount': 100,
        'category': 'INVALID_CATEGORY',  # Directly pass as string
        'transaction_type': TransactionType.CREDIT,
        'description': 'Dinner payment',
        'user_id_token': 1
    }

    # Test data with an invalid transaction type
    data_invalid_type = {
        'amount': 100,
        'category': TransactionCategory.SALARY,
        'transaction_type': 'INVALID_TYPE',  # Directly pass as string
        'description': 'Dinner payment',
        'user_id_token': 1
    }

    # Call the execute function and expect an exception for invalid category
    with pytest.raises(ValueError) as excinfo_category:
        execute(**data_invalid_category)

    # Assert the correct error message
    assert str(excinfo_category.value) == "Invalid category"

    # Call the execute function and expect an exception for invalid transaction type
    with pytest.raises(ValueError) as excinfo_type:
        execute(**data_invalid_type)

    # Assert the correct error message
    assert str(excinfo_type.value) == "Invalid transaction type"