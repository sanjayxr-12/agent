from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase


async def find_policy_by_type(
    db: AsyncIOMotorDatabase, policy_type: str
) -> Optional[Dict[str, Any]]:
    return await db["policy"].find_one(
        {"type": policy_type},
        sort=[("updated_at", -1)],
    )

