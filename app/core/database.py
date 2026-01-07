import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class MongoSingleton:
    _instance: Optional[AsyncIOMotorClient] = None
    _db_name = os.getenv("MONGODB_DB_NAME", "policy")
    _url = os.getenv("MONGODB_URL")

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._instance is None:
            if not cls._url:
                raise RuntimeError("MONGODB_URL not configured")
            cls._instance = AsyncIOMotorClient(cls._url)
            print("INFO: New MongoDB Client created.")
        return cls._instance

    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase:
        client = cls.get_client()
        return client[cls._db_name]

    @classmethod
    def close(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None
            print("INFO: MongoDB Client closed.")

async def get_database() -> AsyncIOMotorDatabase:
    return await MongoSingleton.get_database()

async def close_database_client():
    MongoSingleton.close()