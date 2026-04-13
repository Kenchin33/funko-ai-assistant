from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.complaint import ComplaintRead
from app.services.complaint_service import ComplaintService

router = APIRouter(prefix="/complaints")


@router.post("", response_model=ComplaintRead, status_code=status.HTTP_201_CREATED)
def create_complaint(
    full_name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    order_number: str | None = Form(None),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    files = [file] if file else []

    return ComplaintService.create_complaint(
        db=db,
        full_name=full_name,
        email=email,
        message=message,
        order_number=order_number,
        files=files,
    )