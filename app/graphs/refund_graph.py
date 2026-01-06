from typing import Any, Dict, Optional, TypedDict

from fastapi import HTTPException
from langgraph.graph import END, StateGraph

from app.schemas.policy_schema import PolicySchema
from app.services.intent_service import IntentLabel, detect_intent
from app.services.order_service import (
    get_order,
    initiate_dummy_refund,
    is_order_eligible,
    coerce_purchase_date,
)
from app.services.policy_service import (
    generate_ineligibility_explanation,
    get_refund_policy,
)


class RefundState(TypedDict, total=False):
    message: str
    order_id: str
    intent: IntentLabel
    order: Dict[str, Any]
    policy: PolicySchema
    eligible: bool
    explanation: Optional[str]
    response: Dict[str, Any]


async def detect_intent_node(state: RefundState) -> RefundState:
    intent = await detect_intent(state["message"])
    return {"intent": intent}


def route_intent(state: RefundState) -> str:
    return "REFUND_REQUEST" if state.get("intent") == "REFUND_REQUEST" else "OTHER"


async def fetch_order_node(state: RefundState) -> RefundState:
    print(state)
    order = await get_order(state["order_id"])
    print(order)
    return {"order": order}


async def check_eligibility_node(state: RefundState) -> RefundState:
    policy = await get_refund_policy()
    normalized_date = coerce_purchase_date(state["order"].get("created_at"))
    normalized_order = dict(state["order"], purchase_date=normalized_date)
    eligible = is_order_eligible(normalized_order, policy)
    return {"policy": policy, "eligible": eligible, "order": normalized_order}


def route_eligibility(state: RefundState) -> str:
    return "ELIGIBLE" if state.get("eligible") else "INELIGIBLE"


async def process_refund_node(state: RefundState) -> RefundState:
    result = await initiate_dummy_refund(state["order_id"])
    return {"response": {"status": "success", "message": result["message"]}}


async def generate_explanation_node(state: RefundState) -> RefundState:
    policy = state.get("policy")
    order = state.get("order")
    if not policy or not order:
        raise HTTPException(status_code=500, detail="Policy or order data missing")

    explanation = await generate_ineligibility_explanation(
        policy=policy,
        purchase_date=order["created_at"],
    )
    return {
        "explanation": explanation,
        "response": {"status": "rejected", "message": explanation},
    }


async def generic_response_node(state: RefundState) -> RefundState:
    return {
        "response": {
            "status": "ok",
            "message": "Request received. No refund action required.",
        }
    }


async def finalize_node(state: RefundState) -> RefundState:
    if "response" in state:
        return state
    return {"response": {"status": "error", "message": "No response generated"}}


graph = StateGraph(RefundState)
graph.add_node("detect_intent", detect_intent_node)
graph.add_node("fetch_order", fetch_order_node)
graph.add_node("check_eligibility", check_eligibility_node)
graph.add_node("process_refund", process_refund_node)
graph.add_node("generate_explanation", generate_explanation_node)
graph.add_node("generic_response", generic_response_node)
graph.add_node("finalize", finalize_node)

graph.set_entry_point("detect_intent")
graph.add_conditional_edges(
    "detect_intent",
    route_intent,
    {"REFUND_REQUEST": "fetch_order", "OTHER": "generic_response"},
)
graph.add_edge("generic_response", "finalize")
graph.add_edge("fetch_order", "check_eligibility")
graph.add_conditional_edges(
    "check_eligibility",
    route_eligibility,
    {"ELIGIBLE": "process_refund", "INELIGIBLE": "generate_explanation"},
)
graph.add_edge("process_refund", "finalize")
graph.add_edge("generate_explanation", "finalize")

refund_graph = graph.compile()

