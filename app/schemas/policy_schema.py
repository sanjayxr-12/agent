from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class PolicySchema(BaseModel):
    id: Optional[Any] = Field(default=None, alias="_id")
    type: str
    max_refund_days: int
    policy_text: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

