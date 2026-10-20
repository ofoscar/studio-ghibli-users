from fastapi import FastAPI

from studio_ghibli.api.routes.users import router as users_router

app = FastAPI(
  title = "Studio ghibli users app",
)

app.include_router(users_router, prefix="/api/v1")