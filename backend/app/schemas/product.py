from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    slug: str
    sku: str | None = None
    url: str
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    brand: str | None = None
    series: str | None = None
    character_name: str | None = None
    franchise: str | None = None
    in_stock: bool = True
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    sku: str | None = None
    url: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    brand: str | None = None
    series: str | None = None
    character_name: str | None = None
    franchise: str | None = None
    in_stock: bool | None = None
    is_active: bool | None = None


class ProductRead(ProductBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)