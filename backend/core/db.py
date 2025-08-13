import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    """Create all tables in the database based on SQLAlchemy Base metadata.
    """
    logger.info("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")


async def delete_tables() -> None:
    """Drop all tables from the database.
    """
    logger.info("Dropping tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Tables dropped successfully.")


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Asynchronous context manager that yields a SQLAlchemy AsyncSession.
    """
    logger.info("Creating a new async database session.")
    async with new_session() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Lifespan context manager for FastAPI application.
    """
    await create_tables()
    try:
        yield
    finally:
        logger.info("Application shutdown process complete.")
