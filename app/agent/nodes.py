from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.agent.state import AgentState
from app.agent.tools import list_tables, execute_sql 
from app.utils.gemini_client import get_chat_model, get_gaurd_model
from app.template.agent_prompt_template import guardrails_template, agent_template 
from app.agent.schemas import SafetyAssessment

llm = get_chat_model()
guard_llm = get_gaurd_model() 
llm_with_tools = llm.bind_tools([list_tables, execute_sql])

async def guardrails_node(state: AgentState) -> AgentState:
    question = state["question"]

    structured_llm = guard_llm.with_structured_output(SafetyAssessment)
    
    chain = guardrails_template | structured_llm

    assessment: SafetyAssessment = await chain.ainvoke({"question": question})

    if not assessment.is_safe:
        return {
            "messages": [AIMessage(content=f"Safety Violation: {assessment.reason}")],
            "answer": "Safety Violation: Request blocked.",
            "is_unsafe": True 
        }
    
    return {"is_unsafe": False}

async def agent_node(state: AgentState) -> AgentState:
    messages = state.get("messages", [])

    schema_context = await list_tables.ainvoke({})

    chain = agent_template | llm_with_tools
    
    response = await chain.ainvoke({
        "schema": schema_context,
        "messages": messages
    }, config={"tags":["visible_to_users"]})

    return {"messages": [response]}

async def tools_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    
    if not last_message.tool_calls:
        return {"messages": []} 
    
    results = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]
        
        print(f"DEBUG: AI calling Tool -> {tool_name} with args: {tool_args}")
        
        try:
            if tool_name == "list_tables":
                output = await list_tables.ainvoke(tool_args) 
            elif tool_name == "execute_sql":
                output = await execute_sql.ainvoke(tool_args)
            else:
                output = "Error: Unknown tool."
        except Exception as e:
            output = f"Tool Execution Error: {str(e)}"
            
        results.append(ToolMessage(content=str(output), tool_call_id=tool_call_id))

    return {"messages": results}

def rejection_node(state):
    return {"messages": [AIMessage(content="I cannot answer that as it violates my safety policy.")]}