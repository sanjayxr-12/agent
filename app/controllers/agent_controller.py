from fastapi import APIRouter, HTTPException
from app.agent.graph import agent_graph
from app.agent.state import AgentInput

router = APIRouter()

@router.post("/agent/ask")
async def ask_agent(request: AgentInput):
    try:
        initial_state = {"question": request.question, "messages": []}
        
        result = await agent_graph.ainvoke(initial_state)
        
        last_message = result["messages"][-1]
        final_answer = last_message.content
        
        return {
            "answer": final_answer,
            "history_debug": [m.content for m in result["messages"]] 
        }

    except Exception as e:
        print(f"Agent Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))