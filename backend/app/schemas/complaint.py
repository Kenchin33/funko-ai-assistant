from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ComplaintAttachmentRead(BaseModel):
    id: int
    file_name: str
    mime_type: str
    file_size: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ComplaintRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    order_number: str | None = None
    message: str
    status: str
    created_at: datetime
    attachments: list[ComplaintAttachmentRead] = []

    model_config = ConfigDict(from_attributes=True)