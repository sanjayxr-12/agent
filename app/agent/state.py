from typing import Optional, List, Any, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel
from langgraph.graph.message import add_messages 

class AgentState(TypedDict):
    question: str                   
    sql_query: Optional[str]      
    query_result: Optional[str]    
    retry_count: int             
    messages: Annotated[List[Any], add_messages] 
    answer: Optional[str]
    is_unsafe: Optional[bool] 

class AgentInput(BaseModel):
    question: str
    thread_id: Optional[str] = None