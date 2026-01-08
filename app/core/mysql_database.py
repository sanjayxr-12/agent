import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class MySQLSingleton:
    _engine = None
    _session_maker = None
    _url = os.getenv("MYSQL_URL")

    @classmethod
    def _get_engine(cls):
        if cls._engine is None:
            if not cls._url:
                raise RuntimeError("MYSQL_URL not configured")
            cls._engine = create_async_engine(
                cls._url,
                echo=True,
                pool_pre_ping=True
            )
            print("INFO: New MySQL Engine created.")
        return cls._engine

    @classmethod
    def get_session_maker(cls):
        if cls._session_maker is None:
            engine = cls._get_engine()
            cls._session_maker = sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        return cls._session_maker

async def get_db_session():
    SessionLocal = MySQLSingleton.get_session_maker()
    async with SessionLocal() as session:
        yield session