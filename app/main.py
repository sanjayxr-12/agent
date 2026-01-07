from fastapi import FastAPI
from contextlib import asynccontextmanager
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from app.core.database import close_database_client
from app.agent.graph import workflow 

from app.controllers.agent_controller import router as agent_router 
from app.controllers.refund_controller import router as refund_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO: Connecting to Redis Memory...")
    async with AsyncRedisSaver.from_conn_string("redis://localhost:6379") as checkpointer:
        app.state.agent_graph = workflow.compile(checkpointer=checkpointer)
        print("INFO: Agent Graph Compiled with Redis Memory.")
        
        yield 
        
    print("INFO: Closing Redis Connection...")
    await close_database_client()

app = FastAPI(lifespan=lifespan)

app.include_router(refund_router, prefix="/api")
app.include_router(agent_router, prefix="/api")