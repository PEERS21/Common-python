from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import dotenv_values
config = dotenv_values("/run/secrets/auth/.env")

DATABASE_URL = config.get("DATABASE_URL", "")


ENGINE = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=ENGINE, class_=AsyncSession, expire_on_commit=False)
