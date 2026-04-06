from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.faq import FAQCreate, FAQRead, FAQUpdate
from app.services.faq_service import FAQService

router = APIRouter(prefix="/faq")


@router.post("", response_model=FAQRead, status_code=status.HTTP_201_CREATED)
def create_faq(
    payload: FAQCreate,
    db: Session = Depends(get_db),
):
    return FAQService.create(db, payload)


@router.get("", response_model=list[FAQRead])
def list_faqs(db: Session = Depends(get_db)):
    return FAQService.get_all(db)


@router.get("/admin/all", response_model=list[FAQRead])
def list_all_faqs_admin(db: Session = Depends(get_db)):
    return FAQService.get_all_admin(db)


@router.get("/{faq_id}", response_model=FAQRead)
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = FAQService.get_by_id(db, faq_id)
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ entry not found",
        )
    return faq


@router.put("/{faq_id}", response_model=FAQRead)
def update_faq(
    faq_id: int,
    payload: FAQUpdate,
    db: Session = Depends(get_db),
):
    faq = FAQService.get_by_id(db, faq_id)
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ entry not found",
        )

    return FAQService.update(db, faq, payload)


@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = FAQService.get_by_id(db, faq_id)
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ entry not found",
        )

    FAQService.delete(db, faq)