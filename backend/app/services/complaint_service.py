import os
import shutil
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_attachment import ComplaintAttachment

UPLOAD_DIR = Path("uploads/complaints")
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class ComplaintService:
    @staticmethod
    def _ensure_upload_dir() -> None:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _save_attachment(file: UploadFile) -> tuple[str, str, str]:
        ComplaintService._ensure_upload_dir()

        extension = Path(file.filename or "").suffix.lower()
        mime_type = file.content_type or ""

        if extension not in ALLOWED_EXTENSIONS or mime_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPG, JPEG and PNG files are allowed.",
            )

        unique_name = f"{uuid.uuid4().hex}{extension}"
        file_path = UPLOAD_DIR / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file.filename or unique_name, str(file_path), mime_type

    @staticmethod
    def create_complaint(
        db: Session,
        full_name: str,
        email: str,
        message: str,
        order_number: str | None = None,
        files: list[UploadFile] | None = None,
    ) -> Complaint:
        complaint = Complaint(
            full_name=full_name,
            email=email,
            order_number=order_number,
            message=message,
            status="new",
        )

        db.add(complaint)
        db.flush()

        attachments: list[ComplaintAttachment] = []

        for file in files or []:
            original_name, saved_path, mime_type = ComplaintService._save_attachment(file)

            attachment = ComplaintAttachment(
                complaint_id=complaint.id,
                file_name=original_name,
                file_path=saved_path,
                mime_type=mime_type,
            )
            db.add(attachment)
            attachments.append(attachment)

        db.commit()
        db.refresh(complaint)
        return complaint