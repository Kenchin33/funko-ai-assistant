from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.faq import FAQEntry
from app.schemas.faq import FAQCreate, FAQUpdate


class FAQService:
    @staticmethod
    def create(db: Session, payload: FAQCreate) -> FAQEntry:
        faq = FAQEntry(**payload.model_dump())
        db.add(faq)
        db.commit()
        db.refresh(faq)
        return faq

    @staticmethod
    def get_all(db: Session) -> list[FAQEntry]:
        stmt = select(FAQEntry).order_by(FAQEntry.priority.desc(), FAQEntry.id.asc())
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, faq_id: int) -> FAQEntry | None:
        stmt = select(FAQEntry).where(FAQEntry.id == faq_id)
        return db.scalar(stmt)

    @staticmethod
    def update(db: Session, faq: FAQEntry, payload: FAQUpdate) -> FAQEntry:
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(faq, field, value)

        db.add(faq)
        db.commit()
        db.refresh(faq)
        return faq

    @staticmethod
    def delete(db: Session, faq: FAQEntry) -> None:
        db.delete(faq)
        db.commit()