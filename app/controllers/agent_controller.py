from fastapi import APIRouter, HTTPException, Request 
import uuid
from langchain_core.messages import HumanMessage 
from app.agent.state import AgentInput

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
        
        result = await agent_graph.ainvoke(initial_state, config=config)
        
        last_message = result["messages"][-1]
        final_answer = last_message.content
        
        return {
            "answer": final_answer,
            "thread_id": thread_id, 
            "history_debug": [str(m.content) for m in result["messages"]] 
        }

    except Exception as e:
        print("!!! CRASH DETECTED !!!")
        print(f"Error: {e}")
        try:
            state_snapshot = await agent_graph.aget_state(config)
            if state_snapshot.values.get('messages'):
                print("Last Agent Message:", state_snapshot.values['messages'][-1].content)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))