from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatSessionCreate(BaseModel):
    user_name: str | None = None
    user_email: str | None = None
    source: str | None = None


class ChatSessionRead(BaseModel):
    id: int
    session_token: str
    user_name: str | None = None
    user_email: str | None = None
    source: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatMessageRead(BaseModel):
    id: int
    session_id: int
    role: str
    message_text: str
    detected_intent: str | None = None
    metadata_json: dict | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)