from fastapi import FastAPI
from app.controllers.refund_controller import router as refund_router
from contextlib import asynccontextmanager
from app.core.database import close_database_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await close_database_client()


app = FastAPI(lifespan=lifespan)
app.include_router(refund_router, prefix="/api")