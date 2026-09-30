from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import init_db
from db import async_engine
from routers import router as router
@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
    async_engine.dispose()
app = FastAPI(lifespan=lifespan)
app.include_router(router)


    


