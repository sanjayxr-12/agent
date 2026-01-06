from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


async def find_order_by_id(
    db: AsyncIOMotorDatabase, order_id: str
) -> Optional[Dict[str, Any]]:
    if not ObjectId.is_valid(order_id):
        print(f"Invalid ID format: {order_id}")
        return None

    result = await db["orders"].find_one({"_id": ObjectId(order_id)})
    
    return result

