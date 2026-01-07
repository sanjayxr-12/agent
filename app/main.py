from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import close_database_client

from app.controllers.agent_controller import router as agent_router 
from app.controllers.refund_controller import router as refund_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_database_client()

app = FastAPI(lifespan=lifespan)

app.include_router(refund_router, prefix="/api")
app.include_router(agent_router, prefix="/api")