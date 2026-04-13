from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_attachment import ComplaintAttachment
from app.services.email_service import EmailService

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


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
                detail="File size must not exceed 5 MB.",
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
        complaint = Complaint(
            full_name=full_name,
            email=email,
            order_number=order_number,
            message=message,
            status="new",
        )

        db.add(complaint)
        db.flush()

        for file in files or []:
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
        db.refresh(complaint)

        try:
            EmailService.send_complaint_to_support(complaint)
            EmailService.send_complaint_confirmation_to_client(complaint)
        except Exception as exc:
            print("EMAIL ERROR:", exc)

        return complaint