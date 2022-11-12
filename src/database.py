from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from config import postgres_url

engine = create_async_engine(postgres_url)
ASession = sessionmaker(autocommit=False, expire_on_commit=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db() -> Session:
    async with ASession() as session:
        yield session
