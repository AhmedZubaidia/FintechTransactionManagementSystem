import pytest
from unittest.mock import patch
from app.logic.user.profile.admin.get_all_users import execute


# Mock the paginated query result
class MockPaginate:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total


class MockQuery:
    def paginate(self, page, per_page, error_out):
        return MockPaginate(items=[{'id': 1, 'name': 'User1'}, {'id': 2, 'name': 'User2'}],
                            page=page, per_page=per_page, total=2)


class MockUser:
    query = MockQuery()


# Patch the User model in the module where the execute function is located
@patch('app.logic.user.profile.admin.get_all_users.User', new=MockUser)
def test_execute_get_all_users():
    page = 1
    per_page = 10

    result = execute(page, per_page)

    assert result.items == [{'id': 1, 'name': 'User1'}, {'id': 2, 'name': 'User2'}]
    assert result.page == 1
    assert result.per_page == 10
    assert result.total == 2
