from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.text import normalize_text


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
    def search(db: Session, query: str) -> list[Product]:
        normalized_query = normalize_text(query)
        like_query = f"%{normalized_query}%"

        stmt = (
            select(Product)
            .where(
                Product.is_active.is_(True),
                or_(
                    Product.title.ilike(like_query),
                    Product.sku.ilike(like_query),
                    Product.character_name.ilike(like_query),
                    Product.franchise.ilike(like_query),
                    Product.series.ilike(like_query),
                ),
            )
            .order_by(Product.in_stock.desc(), Product.id.asc())
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def exact_lookup(db: Session, query: str) -> Product | None:
        normalized_query = normalize_text(query)

        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.in_stock.desc(), Product.id.asc())
        )

        products = list(db.scalars(stmt).all())

        for product in products:
            title = normalize_text(product.title or "")
            sku = normalize_text(product.sku or "")
            combined = normalize_text(f"{product.title or ''} {product.sku or ''}")

            if normalized_query == title:
                return product
            if sku and normalized_query == sku:
                return product
            if normalized_query == combined:
                return product

        return None