from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for the Funko AI Assistant project.",
)

app.include_router(api_router, prefix="")


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running",
        "environment": settings.APP_ENV,
    }