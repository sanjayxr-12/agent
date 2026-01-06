from typing import Literal, Set
from enum import Enum
from pydantic import BaseModel

from app.utils.gemini_client import generate_text

IntentLabel = Literal["REFUND_REQUEST", "OTHER"]
INTENT_LABELS: Set[str] = {"REFUND_REQUEST", "OTHER"}

class IntentLabel(str, Enum):
    REFUND_REQUEST = "REFUND_REQUEST"
    OTHER = "OTHER"

class IntentPrediction(BaseModel):
    intent: IntentLabel

async def detect_intent(message: str) -> IntentLabel:
    prompt = f"Analyze this user message and classify the intent: {message}"
    
    result: IntentPrediction = await generate_text(
        prompt=prompt,
        response_schema=IntentPrediction
    )

    print(result.intent)
    
    if result:
        return result.intent

