from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.text import normalize_text
from app.services.product_alias_service import ProductAliasService


class ProductService:
    @staticmethod
    def create(db: Session, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all(db: Session) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.in_stock.desc(), Product.id.asc())
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        return db.scalar(stmt)

    @staticmethod
    def update(db: Session, product: Product, payload: ProductUpdate) -> Product:
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()

    @staticmethod
    def _clean_search_query(query: str) -> str:
        normalized = normalize_text(query)

        noise_phrases = [
            "які є фігурки по",
            "які є по",
            "що є по",
            "покажи",
            "знайди",
            "які є",
            "що є",
            "є",
            "чи є",
            "funko pop",
            "фігурки",
            "фігурка",
        ]

        cleaned = normalized
        for phrase in noise_phrases:
            cleaned = cleaned.replace(phrase, " ")

        cleaned = " ".join(cleaned.split())
        return cleaned

    @staticmethod
    def search(db: Session, query: str) -> list[Product]:
        aliases = ProductAliasService.find_alias_matches(db, query)

        filters = []

        for alias in aliases:
            if alias.target_type == "character":
                filters.append(Product.character_name.ilike(f"%{alias.target_value}%"))

            elif alias.target_type == "franchise":
                filters.append(Product.franchise.ilike(f"%{alias.target_value}%"))

            elif alias.target_type == "series":
                filters.append(Product.series.ilike(f"%{alias.target_value}%"))

        if filters:
            stmt = (
                select(Product)
                .where(Product.is_active.is_(True))
                .where(or_(*filters))
                .order_by(Product.in_stock.desc(), Product.id.asc())
            )
            return list(db.scalars(stmt).all())

        # fallback — старий пошук
        return []

    @staticmethod
    def exact_lookup(db: Session, query: str) -> Product | None:
        aliases = ProductAliasService.find_alias_matches(db, query)

        for alias in aliases:
            if alias.target_type == "product" and alias.product_id:
                stmt = select(Product).where(Product.id == alias.product_id)
                return db.scalar(stmt)

        return None