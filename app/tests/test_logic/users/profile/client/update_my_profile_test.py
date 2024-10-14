import pytest
from unittest.mock import patch, MagicMock
from app.logic.user.profile.client.update_my_profile import execute


# Mock class to simulate a user object
class MockUser:
    def __init__(self, id, username='current_user', deleted_at=None):
        self.id = id
        self.username = username
        self.deleted_at = deleted_at


class MockQuery:
    def get(self, user_id):
        if user_id == 1:
            return MockUser(id=user_id)  # User found
        return None  # User not found

    def filter_by(self, **kwargs):
        # Simulate a query with .first() method
        if kwargs.get("username") == "new_username":
            mock_existing_user = MockUser(id=2, username="new_username")
            query = MagicMock()
            query.first.return_value = mock_existing_user  # Simulate the first result
            return query
        query = MagicMock()
        query.first.return_value = None  # Simulate no result
        return query


class MockDb:
    def commit(self):
        pass


# Test for updating profile successfully
@patch('app.logic.user.profile.client.update_my_profile.User', new=MockUser)
@patch('app.logic.user.profile.client.update_my_profile.db', new=MockDb)
def test_execute_update_my_profile_success():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to MockUser class
    MockDb.session = MockDb()  # Attach mock db session to MockDb class





    # Test data
    data = {'user_id': 1, 'username': 'new_user'}

    # Call the execute function
    result = execute(**data)

    # Assertions
    assert result['message'] == "Profile updated successfully"
    assert result['user_id'] == 1


# Test for email update not allowed
@patch('app.logic.user.profile.client.update_my_profile.User', new=MockUser)
@patch('app.logic.user.profile.client.update_my_profile.db', new=MockDb)
def test_execute_update_my_profile_email_not_allowed():
    mock_query = MockQuery()
    MockUser.query = mock_query  # Attach mock query to MockUser class

    # Test data where email is included
    data = {'user_id': 1, 'email': 'newemail@example.com'}

    # Call the execute function
    result = execute(**data)

    # Assertions
    assert result['errors'] == "Changing email is not allowed"


# Test for username already taken
@patch('app.logic.user.profile.client.update_my_profile.User', new=MockUser)
@patch('app.logic.user.profile.client.update_my_profile.db', new=MockDb)
def test_execute_update_my_profile_username_taken():
    mock_query = MockQuery()  # Mock query to simulate user search
    MockUser.query = mock_query  # Attach mock query to MockUser class

    # Test data where username is already taken
    data = {'user_id': 1, 'username': 'new_username'}

    # Call the execute function
    result = execute(**data)

    # Assertions
    assert result['errors'] == "Username is already taken"
