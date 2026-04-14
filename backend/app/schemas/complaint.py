from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

ComplaintStatus = Literal["new", "in_progress", "resolved", "rejected"]


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
    status: ComplaintStatus
    created_at: datetime
    attachments: list[ComplaintAttachmentRead] = []

    model_config = ConfigDict(from_attributes=True)


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus