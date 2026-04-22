from pydantic import EmailStr
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.complaint_attachment import ComplaintAttachment
from app.schemas.complaint import ComplaintRead, ComplaintStatusUpdate
from app.services.complaint_service import ComplaintService

router = APIRouter(prefix="/complaints")
admin_router = APIRouter(prefix="/admin/complaints")


@router.post("", response_model=ComplaintRead, status_code=status.HTTP_201_CREATED)
def create_complaint(
    full_name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...),
    order_number: str | None = Form(None),
    files: list[UploadFile] | None = File(default=None),
    db: Session = Depends(get_db),
):
    return ComplaintService.create_complaint(
        db=db,
        full_name=full_name,
        email=str(email),
        message=message,
        order_number=order_number,
        files=files,
    )


@router.get("/attachments/{attachment_id}")
def get_complaint_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
):
    stmt = select(ComplaintAttachment).where(ComplaintAttachment.id == attachment_id)
    attachment = db.scalar(stmt)

    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found",
        )

    if not attachment.file_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment has no file content",
        )

    return Response(
        content=attachment.file_content,
        media_type=attachment.mime_type,
        headers={"Content-Disposition": "inline"},
    )


@admin_router.get("", response_model=list[ComplaintRead])
def list_complaints(db: Session = Depends(get_db)):
    return ComplaintService.get_all(db)


@admin_router.get("/{complaint_id}", response_model=ComplaintRead)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = ComplaintService.get_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found",
        )
    return complaint


@admin_router.patch("/{complaint_id}/status", response_model=ComplaintRead)
def update_complaint_status(
    complaint_id: int,
    payload: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
):
    complaint = ComplaintService.get_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found",
        )

    return ComplaintService.update_status(db, complaint, payload.status)