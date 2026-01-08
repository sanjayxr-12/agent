from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse 
import uuid
from langchain_core.messages import HumanMessage
from app.agent.state import AgentInput
from app.utils.stream_writer import run_agent_stream 

router = APIRouter()

@router.post("/agent/ask")
async def ask_agent(request: AgentInput, req: Request):
    try:
        thread_id = request.thread_id or str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 50}
        
        initial_state = {
            "question": request.question,
            "messages": [HumanMessage(content=request.question)]
        }
        
        agent_graph = req.app.state.agent_graph
    
        return StreamingResponse(
            run_agent_stream(agent_graph, initial_state, config, thread_id),
            media_type="text/event-stream"
        )

    except Exception as e:
        print("!!! CRASH DETECTED !!!")
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))