from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProductAlias(Base):
    __tablename__ = "product_aliases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    alias: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alias_normalized: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_value: Mapped[str] = mapped_column(String(255), nullable=False)

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)