from fastapi import APIRouter

from app.api.routes.db_test import router as db_test_router
from app.api.routes.health import router as health_router
from app.api.routes.setup import router as setup_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_PREFIX)

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(db_test_router, tags=["Database"])
api_router.include_router(setup_router, tags=["Setup"])