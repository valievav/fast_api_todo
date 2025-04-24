from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src_db.config import Config

engine = create_async_engine(url=Config.DATABASE_URL, echo=True)


async def create_connection():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_connection()
    yield


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)

    async with Session(bind=engine) as session:
        yield session
