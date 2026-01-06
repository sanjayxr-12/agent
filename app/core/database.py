import os
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "policy")

_client: Optional[AsyncIOMotorClient] = None


async def get_database() -> AsyncIOMotorDatabase:
    global _client
    if not MONGODB_URL:
        raise RuntimeError("MONGODB_URL not configured")

    if _client is None:
        _client = AsyncIOMotorClient(MONGODB_URL)
    return _client[MONGODB_DB_NAME]


async def close_database_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

