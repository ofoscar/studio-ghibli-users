import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager

from studio_ghibli.api.routes.users import router as users_router
from studio_ghibli.api.routes.auth import router as auth_router
from studio_ghibli.core.bootstrap import ensure_admin_exists
from studio_ghibli.core.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app:FastAPI):
  create_db_and_tables()
  ensure_admin_exists()

  async with httpx.AsyncClient(timeout=10.0) as client:
    app.state.http_client = client
    yield

app = FastAPI(
  title = "Studio ghibli users app",
  lifespan=lifespan
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")