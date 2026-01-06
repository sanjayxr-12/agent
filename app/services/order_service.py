from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import HTTPException

from app.core.database import get_database
from app.repositories.order_repository import find_order_by_id
from app.schemas.policy_schema import PolicySchema


async def get_order(order_id: str) -> Dict[str, Any]:
    db = await get_database()
    order = await find_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def coerce_purchase_date(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    try:
        print(value)
        return datetime.fromisoformat(str(value))
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=400, detail="Invalid purchase_date format") from exc


def is_order_eligible(order: Dict[str, Any], policy: PolicySchema) -> bool:
    purchase_date = coerce_purchase_date(order.get("purchase_date"))
    if purchase_date.tzinfo is None:
        purchase_date = purchase_date.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days_since_purchase = (now - purchase_date).days
    return days_since_purchase <= policy.max_refund_days


async def initiate_dummy_refund(order_id: str) -> Dict[str, str]:
    return {"status": "success", "message": f"Refund initiated for order {order_id}"}

