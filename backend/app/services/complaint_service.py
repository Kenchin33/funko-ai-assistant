from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.complaint import Complaint
from app.models.complaint_attachment import ComplaintAttachment
from app.services.email_service import EmailService

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_FILES_COUNT = 3

ALLOWED_STATUS_TRANSITIONS = {
    "new": {"in_progress"},
    "in_progress": {"resolved", "rejected"},
    "resolved": set(),
    "rejected": set(),
}


class ComplaintService:
    @staticmethod
    def _validate_file(file: UploadFile, content: bytes) -> tuple[str, str, int]:
        file_name = file.filename or "attachment"
        extension = f".{file_name.split('.')[-1].lower()}" if "." in file_name else ""
        mime_type = file.content_type or ""
        file_size = len(content)

        if extension not in ALLOWED_EXTENSIONS or mime_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPG, JPEG and PNG files are allowed.",
            )

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each file size must not exceed 5 MB.",
            )

        return file_name, mime_type, file_size

    @staticmethod
    def create_complaint(
        db: Session,
        full_name: str,
        email: str,
        message: str,
        order_number: str | None = None,
        files: list[UploadFile] | None = None,
    ) -> Complaint:
        files = files or []

        if len(files) > MAX_FILES_COUNT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can upload a maximum of 3 files.",
            )

        complaint = Complaint(
            full_name=full_name,
            email=email,
            order_number=order_number,
            message=message,
            status="new",
        )

        db.add(complaint)
        db.flush()

        for file in files:
            content = file.file.read()
            file_name, mime_type, file_size = ComplaintService._validate_file(file, content)

            attachment = ComplaintAttachment(
                complaint_id=complaint.id,
                file_name=file_name,
                mime_type=mime_type,
                file_size=file_size,
                file_content=content,
            )
            db.add(attachment)

        db.commit()

        stmt = (
            select(Complaint)
            .options(selectinload(Complaint.attachments))
            .where(Complaint.id == complaint.id)
        )
        complaint = db.scalar(stmt)

        try:
            if complaint is not None:
                EmailService.send_complaint_to_support(complaint)
                EmailService.send_complaint_confirmation_to_client(complaint)
        except Exception as exc:
            print("EMAIL ERROR:", exc)

        if complaint is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Complaint was created but could not be reloaded.",
            )

        return complaint

    @staticmethod
    def get_all(db: Session) -> list[Complaint]:
        stmt = (
            select(Complaint)
            .options(selectinload(Complaint.attachments))
            .order_by(Complaint.created_at.desc(), Complaint.id.desc())
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, complaint_id: int) -> Complaint | None:
        stmt = (
            select(Complaint)
            .options(selectinload(Complaint.attachments))
            .where(Complaint.id == complaint_id)
        )
        return db.scalar(stmt)

    @staticmethod
    def update_status(db: Session, complaint: Complaint, new_status: str) -> Complaint:
        current_status = complaint.status

        if new_status == current_status:
            return complaint

        allowed_next_statuses = ALLOWED_STATUS_TRANSITIONS.get(current_status, set())

        if new_status not in allowed_next_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Status transition from '{current_status}' to '{new_status}' is not allowed."
                ),
            )

        complaint.status = new_status
        db.add(complaint)
        db.commit()

        stmt = (
            select(Complaint)
            .options(selectinload(Complaint.attachments))
            .where(Complaint.id == complaint.id)
        )
        refreshed = db.scalar(stmt)
        if refreshed is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Complaint status updated but could not be reloaded.",
            )
        return refreshed