import pytest
from unittest.mock import patch
from app.logic.user.profile.admin.delete_user import execute
from datetime import datetime


# Mock class to simulate a user object
class MockUser:
    def __init__(self, id, is_deleted=False):
        self.id = id
        self.is_deleted = is_deleted
        self.deleted_at = None

    # Simulate soft deletion
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True


class MockQuery:
    def get(self, user_id):
        if user_id == 1:
            return MockUser(id=user_id, is_deleted=False)  # User found and not deleted
        return None  # Simulate user not found


# Mock the db.session.commit()
class MockSession:
    def commit(self):
        pass


class MockDb:
    session = MockSession()


# Patch the User model and db.session in the module where the delete function is located
@patch('app.logic.user.profile.admin.delete_user.User', new=MockUser)
@patch('app.logic.user.profile.admin.delete_user.db', new=MockDb)
def test_execute_delete_user_success():
    # Mocking the user and the query behavior
    mock_query = MockQuery()
    MockUser.query = mock_query

    # Call the execute function to delete user with ID 1
    result = execute(1)

    assert result['message'] == "User soft deleted successfully"


# Test for user not found case
@patch('app.logic.user.profile.admin.delete_user.User', new=MockUser)
@patch('app.logic.user.profile.admin.delete_user.db', new=MockDb)
def test_execute_delete_user_not_found():
    mock_query = MockQuery()
    MockUser.query = mock_query

    # Execute with user_id that doesn't exist
    result = execute(999)
    assert result['errors'] == "User not found"


# Test for user already deleted
@patch('app.logic.user.profile.admin.delete_user.User', new=MockUser)
@patch('app.logic.user.profile.admin.delete_user.db', new=MockDb)
def test_execute_delete_user_already_deleted():
    class MockQueryWithDeletedUser(MockQuery):
        def get(self, user_id):
            return MockUser(id=user_id, is_deleted=True)  # User already deleted

    MockUser.query = MockQueryWithDeletedUser()

    # Call the execute function to delete an already deleted user
    result = execute(1)

    assert result['errors'] == "User is already deleted"
