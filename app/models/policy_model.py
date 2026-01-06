from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PolicySchema(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    type: str
    max_refund_days: int
    policy_text: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
    