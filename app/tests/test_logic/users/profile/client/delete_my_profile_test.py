import pytest
from unittest.mock import patch
from app.logic.user.profile.client.delete_my_profile import execute
from datetime import datetime


# Mock class to simulate a user object
class MockUser:
    def __init__(self, id, deleted_at=None):
        self.id = id
        self.deleted_at = deleted_at


class MockQuery:
    def get(self, user_id):
        if user_id == 1:
            return MockUser(id=user_id, deleted_at=None)  # User found and not deleted
        if user_id == 2:
            return MockUser(id=user_id, deleted_at=datetime.utcnow())  # User already deleted
        return None  # User not found


class MockDb:
    def commit(self):
        pass


# Test for successful profile deletion
@patch('app.logic.user.profile.client.delete_my_profile.User', new=MockUser)
@patch('app.logic.user.profile.client.delete_my_profile.db', new=MockDb)
def test_execute_delete_my_profile_success():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach the mock query to the MockUser class
    MockDb.session = MockDb()  # Attach the mock db session to the MockDb class

    # Call the execute function to delete the profile with user_id = 1
    result = execute(user_id=1)

    # Assert the expected output
    assert result['message'] == "Profile soft deleted successfully"


# Test for user not found
@patch('app.logic.user.profile.client.delete_my_profile.User', new=MockUser)
@patch('app.logic.user.profile.client.delete_my_profile.db', new=MockDb)
def test_execute_delete_my_profile_not_found():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach the mock query to the MockUser class

    # Call the execute function with a non-existent user_id
    result = execute(user_id=999)

    # Assert the expected output
    assert result['errors'] == "User not found"


# Test for user already deleted
@patch('app.logic.user.profile.client.delete_my_profile.User', new=MockUser)
@patch('app.logic.user.profile.client.delete_my_profile.db', new=MockDb)
def test_execute_delete_my_profile_already_deleted():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach the mock query to the MockUser class

    # Call the execute function with user_id = 2 (already deleted user)
    result = execute(user_id=2)

    # Assert the expected output
    assert result['errors'] == "User is already deleted"
