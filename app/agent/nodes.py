from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from app.agent.state import AgentState
from app.agent.tools import list_tables, execute_sql 
from app.utils.gemini_client import get_chat_model

llm = get_chat_model() 
llm_with_tools = llm.bind_tools([list_tables, execute_sql])

async def agent_node(state: AgentState) -> AgentState:
    messages = state.get("messages", [])
    question = state["question"]
    
    if not messages:
        print("DEBUG: Fetching schema for System Prompt...")
        schema_context = await list_tables.ainvoke({})  
        system_prompt = (
            "You are a MySQL Expert. "
            "Use the provided tools to answer the user's question. "
            "NEVER guess column names. Always refer to the schema below.\n\n"
            "### DATABASE SCHEMA ###\n"
            f"{schema_context}"
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]

    response = await llm_with_tools.ainvoke(messages)
    
    return {"messages": messages + [response]}

async def tools_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    
    if not last_message.tool_calls:
        return state 
    
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
    
    return {"messages": state["messages"] + results}