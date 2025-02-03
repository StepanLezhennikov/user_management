from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
