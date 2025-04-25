import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src_db import app, base_url
from src_db.config import Config
from src_db.db.main import get_session

test_engine = create_async_engine(
    url=Config.TEST_DATABASE_URL,
    echo=True
)


@pytest.fixture(autouse=True)
def set_test_env():
    # need to add test-specific flag, that will be used by for lifespan from src_db.db.main
    # this is needed, so lifespan won't trigger creation of the main_db during app instantiation
    # before that we had 2 dbs instantiated during test run - test_db (where tests run) and main_db (inactive)
    os.environ["IS_TEST_ENV"] =  '1'
    yield
    del os.environ["IS_TEST_ENV"]  # reset after tests


# create a session to override the default db session
async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)

    async with Session(bind=test_engine) as session:
        yield session


@pytest_asyncio.fixture
async def test_client(set_test_env):
    """
    Test app client
    """
    async with test_engine.begin() as conn:
        # double-check we are on test db, since we are going to drop all tables
        db_name = make_url(str(test_engine.url)).database
        is_test_db = db_name.lstrip('./') == Config.TEST_DATABASE_URL.split('/')[-1]
        if not is_test_db:
            yield

        await conn.run_sync(SQLModel.metadata.drop_all)  # to have clean state
        await conn.run_sync(SQLModel.metadata.create_all)

    # override session
    app.dependency_overrides[get_session] = test_get_session

    with TestClient(app) as client:
        yield client


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


@pytest.fixture
def existing_todo_entry(test_client, test_todo_item_payload):
    response = test_client.post(f'{base_url}', json=test_todo_item_payload)
    return response.json()
