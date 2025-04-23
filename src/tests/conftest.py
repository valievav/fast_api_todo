import copy

import pytest
from fastapi.testclient import TestClient

from src import app
from src.data import all_todos, get_all_todos


@pytest.fixture(autouse=True, scope='module')
def test_client():
    """
    Test app client
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True, scope='function')
def test_data():
    """
    Return test data as fixture to recreate it on each test
    (so previous test doesn't affect next) AND so we don't edit real data.
    """
    test_todos = copy.deepcopy(get_all_todos())
    # make sure these are different objects - so real data is not affected
    assert test_todos is not all_todos

    app.dependency_overrides[get_all_todos] = lambda: test_todos

    yield test_todos

    app.dependency_overrides.clear()


@pytest.fixture
def test_todo_item_payload():
    """
    Payload for todo item creation
    """
    payload = {
        'description': 'Write tests',
        'priority': 2,
    }
    return payload
