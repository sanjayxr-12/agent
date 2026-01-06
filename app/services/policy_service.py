from datetime import datetime

from fastapi import HTTPException

from app.core.database import get_database
from app.repositories.policy_repository import find_policy_by_type
from app.schemas.policy_schema import PolicySchema
from app.utils.gemini_client import generate_text


async def get_refund_policy() -> PolicySchema:
    db = await get_database()
    document = await find_policy_by_type(db, "REFUND_POLICY")
    if not document:
        raise HTTPException(status_code=404, detail="Refund policy not configured")
    return PolicySchema.model_validate(document)


async def generate_ineligibility_explanation(
    policy: PolicySchema, purchase_date: datetime
) -> str:
    prompt = (
        "You are a helpful support agent. Explain briefly why this refund "
        "request is not eligible, using the provided policy only.\n"
        f"Policy: {policy.policy_text}\n"
        f"Purchase date: {purchase_date.date().isoformat()}\n"
        f"Max refund days: {policy.max_refund_days}\n"
        "Keep it concise (under 80 words) and avoid policy changes."
    )
    return await generate_text(prompt)

