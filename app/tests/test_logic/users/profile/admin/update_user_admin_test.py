import pytest
from unittest.mock import patch
from app.logic.user.profile.admin.update_user import execute
from datetime import datetime


# Mock class to simulate a user object
class MockUser:
    def __init__(self, id, is_deleted=False):
        self.id = id
        self.is_deleted = is_deleted
        self.deleted_at = None
        self.name = None
        self.email = None

    # Simulate updating user attributes
    def update(self, **data):
        for key, value in data.items():
            setattr(self, key, value)


class MockQuery:
    def get(self, user_id):
        if user_id == 1:
            return MockUser(id=user_id, is_deleted=False)  # User found
        return None  # Simulate user not found


# Mock the db.session.commit() to simulate a database commit
class MockSession:
    def commit(self):
        pass


class MockDb:
    session = MockSession()


# Test for successful user update
@patch('app.logic.user.profile.admin.update_user.User', new=MockUser)  # Mock the User model
@patch('app.logic.user.profile.admin.update_user.db', new=MockDb)  # Mock the db session
def test_execute_update_user_success():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to the MockUser class

    # Call the execute function to update user with ID 1
    data = {'name': 'New Name', 'email': 'newemail@example.com'}
    result = execute(1, **data)

    # Assert the correct message and updated user_id
    assert result['message'] == "User updated successfully"
    assert result['user_id'] == 1


# Test for user not found
@patch('app.logic.user.profile.admin.update_user.User', new=MockUser)  # Mock the User model
@patch('app.logic.user.profile.admin.update_user.db', new=MockDb)  # Mock the db session
def test_execute_update_user_not_found():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to the MockUser class

    # Call the execute function with a user_id that doesn't exist
    data = {'name': 'New Name', 'email': 'newemail@example.com'}
    result = execute(999, **data)

    # Assert the correct error message is returned
    assert result['errors'] == "User not found"
