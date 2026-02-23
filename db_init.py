from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

ENGINE = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=ENGINE, class_=AsyncSession, expire_on_commit=False)
