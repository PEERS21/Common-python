from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv

DATABASE_URL = f"mysql+aiomysql://{getenv("SERVICE_NAME", "changeme")}:{getenv("SERVICE_PASS", "changeme")}@{getenv("DB_HOST", "changeme")}:3306/{getenv("DB_NAME", "changeme")}?charset=utf8mb4"

ENGINE = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=ENGINE, class_=AsyncSession, expire_on_commit=False)
