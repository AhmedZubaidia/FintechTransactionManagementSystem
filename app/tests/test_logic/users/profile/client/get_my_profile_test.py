import pytest
from unittest.mock import patch
from app.logic.user.profile.client.get_my_profile import execute


# Mock class to simulate a user object
class MockUser:
    def __init__(self, id, deleted_at=None):
        self.id = id
        self.deleted_at = deleted_at


class MockQuery:
    def get(self, user_id):
        if user_id == 1:
            return MockUser(id=user_id, deleted_at=None)  # User found
        if user_id == 2:
            return MockUser(id=user_id, deleted_at='2024-01-01')  # User soft-deleted
        return None  # User not found


# Test for getting user profile successfully
@patch('app.logic.user.profile.client.get_my_profile.User', new=MockUser)
def test_execute_get_my_profile_success():
    mock_query = MockQuery()
    MockUser.query = mock_query

    result = execute(1)
    assert result.id == 1


# Test for user not found
@patch('app.logic.user.profile.client.get_my_profile.User', new=MockUser)
def test_execute_get_my_profile_not_found():
    mock_query = MockQuery()
    MockUser.query = mock_query

    with pytest.raises(Exception) as excinfo:
        execute(999)
    assert "User with ID 999 not found" in str(excinfo.value)


# Test for user already deleted
@patch('app.logic.user.profile.client.get_my_profile.User', new=MockUser)
def test_execute_get_my_profile_deleted():
    mock_query = MockQuery()
    MockUser.query = mock_query

    with pytest.raises(Exception) as excinfo:
        execute(2)
    assert "User with ID 2 not found" in str(excinfo.value)
