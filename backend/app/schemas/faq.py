from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FAQBase(BaseModel):
    category: str
    question: str
    answer: str
    keywords: str | None = None
    button_label: str | None = None
    button_url: str | None = None
    priority: int = 0
    is_active: bool = True


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    category: str | None = None
    question: str | None = None
    answer: str | None = None
    keywords: str | None = None
    button_label: str | None = None
    button_url: str | None = None
    priority: int | None = None
    is_active: bool | None = None


class FAQRead(FAQBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)