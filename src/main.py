from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.v1 import products
from src.core.database import engine, Base
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="NeoMarket B2C Catalog",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(products.router, prefix="/api/v1", tags=["products"])