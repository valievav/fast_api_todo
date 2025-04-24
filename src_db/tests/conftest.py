from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src_db import app
from src_db import base_url
from src_db.config import Config
from src_db.db.main import get_session

test_engine = create_async_engine(
    url=Config.TEST_DATABASE_URL,
    echo=True
)


# create a session to override the default db session
async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)

    async with Session(bind=test_engine) as session:
        yield session


@pytest_asyncio.fixture #(scope='function')
async def test_client():
    """
    Test app client
    """
    async with test_engine.begin() as conn:
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
