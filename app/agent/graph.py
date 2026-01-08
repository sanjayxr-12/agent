from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import agent_node, tools_node, guardrails_node

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

def check_safety(state: AgentState) -> str:
    if state.get("is_unsafe"):
        return END 
    return "agent"

workflow = StateGraph(AgentState)

workflow.add_node("guardrails", guardrails_node)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tools_node)

workflow.set_entry_point("guardrails")

workflow.add_conditional_edges("guardrails", check_safety, {END: END, "agent": "agent"})
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")
