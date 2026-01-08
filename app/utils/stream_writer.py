import json
from langchain_core.messages import AIMessageChunk, AIMessage

async def run_agent_stream(graph, input_state, config, thread_id):
    try:
        metadata_payload = {
            "type": "thread_id",
            "content": thread_id
        }
        yield f"data: {json.dumps(metadata_payload)}\n\n"

        async for event in graph.astream_events(input_state, config=config, version="v2"):
            kind = event["event"]
            tags = event.get("tags",[])
  
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]

                if "visible_to_users" in tags:
                    if isinstance(chunk, AIMessageChunk) and chunk.content:
                        payload = {
                            "type": "token",
                            "content": chunk.content
                        }
                        yield f"data: {json.dumps(payload)}\n\n"

            elif kind == "on_tool_start":
                tool_name = event["name"]
                if tool_name and not tool_name.startswith("_"):
                    payload = {
                        "type": "status",
                        "content": f"Executing tool: {tool_name}..."
                    }
                    yield f"data: {json.dumps(payload)}\n\n"
            elif kind == "on_tool_end":
                tool_name = event["name"]
                if tool_name and not tool_name.startswith("_"):
                    payload = {
                        "type": "status",
                        "content": f"{tool_name} completed."
                    }
                    yield f"data: {json.dumps(payload)}\n\n"

            elif event["event"] == "on_chain_end" and event["name"] == "rejection":
                messages = event["data"]["output"].get("messages", [])
                if messages:
                    last_message = messages[-1]
                    if isinstance(last_message, AIMessage):
                        yield json.dumps({"type": "token", "content": last_message.content})        

    except Exception as e:
        error_payload = {
            "type": "error",
            "content": f"Stream Error: {str(e)}"
        }
        yield f"data: {json.dumps(error_payload)}\n\n"
    
    finally:
        yield "data: [DONE]\n\n"