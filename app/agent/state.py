from typing import Optional, List, Any, Dict
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    question: str                   
    sql_query: Optional[str]      
    query_result: Optional[str]    
    retry_count: int             
    messages: List[Any]       
    answer: Optional[str]

class AgentInput(BaseModel):
    question: str

class AgentOutput(BaseModel):
    answer: str
    sql_used: str