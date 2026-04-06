from fastapi import APIRouter

from app.core.init_db import init_db

router = APIRouter()


@router.post("/setup/init-db")
def setup_database():
    init_db()
    return {"status": "ok", "message": "Database tables created successfully"}