from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
import os

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./advertisements.db")

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    poolclass=StaticPool
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session