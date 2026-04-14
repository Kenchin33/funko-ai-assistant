from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.db_test import router as db_test_router
from app.api.routes.faq import router as faq_router
from app.api.routes.health import router as health_router
from app.api.routes.products import router as products_router
from app.api.routes.setup import router as setup_router
from app.core.config import settings
from app.api.routes.complaints import (
    admin_router as admin_complaints_router,
    router as complaints_router,
)

api_router = APIRouter(prefix=settings.API_PREFIX)

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(db_test_router, tags=["Database"])
api_router.include_router(setup_router, tags=["Setup"])
api_router.include_router(faq_router, tags=["FAQ"])
api_router.include_router(chat_router, tags=["Chat"])
api_router.include_router(products_router, tags=["Products"])
api_router.include_router(complaints_router, tags=["Complaints"])
api_router.include_router(admin_complaints_router, tags=["Admin Complaints"])