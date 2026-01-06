from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.graphs.refund_graph import refund_graph


router = APIRouter()


class RefundRequest(BaseModel):
    message: str = Field(..., min_length=1)
    order_id: str = Field(..., min_length=1)


@router.post("/refund")
async def process_refund(request: RefundRequest):
    try:
        result = await refund_graph.ainvoke(
            {"message": request.message, "order_id": request.order_id}
        )
    except HTTPException:
        raise
    except Exception as exc: 
        print(exc)
        raise HTTPException(status_code=500, detail="Error")

    return result.get("response", {"status": "error", "message": "No response generated"})

