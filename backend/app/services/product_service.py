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
        cleaned_query = ProductService._clean_search_query(query)

        if not cleaned_query:
            return []

        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.in_stock.desc(), Product.id.asc())
        )
        products = list(db.scalars(stmt).all())

        query_tokens = set(cleaned_query.split())
        matched_products: list[tuple[int, Product]] = []

        for product in products:
            searchable_text = normalize_text(
                " ".join(
                    [
                        product.title or "",
                        product.sku or "",
                        product.character_name or "",
                        product.franchise or "",
                        product.series or "",
                    ]
                )
            )

            score = 0

            if cleaned_query in searchable_text:
                score += 50

            for token in query_tokens:
                if token in searchable_text:
                    score += 15

            if score > 0:
                matched_products.append((score, product))

        matched_products.sort(key=lambda item: (-item[0], not item[1].in_stock, item[1].id))
        return [product for _, product in matched_products]

    @staticmethod
    def exact_lookup(db: Session, query: str) -> Product | None:
        cleaned_query = ProductService._clean_search_query(query)

        if not cleaned_query:
            return None

        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.in_stock.desc(), Product.id.asc())
        )

        products = list(db.scalars(stmt).all())

        for product in products:
            title = normalize_text(product.title or "")
            sku = normalize_text(product.sku or "")
            character_name = normalize_text(product.character_name or "")
            combined_title_sku = normalize_text(f"{product.title or ''} {product.sku or ''}")
            combined_character_sku = normalize_text(f"{product.character_name or ''} {product.sku or ''}")

            if cleaned_query == title:
                return product
            if sku and cleaned_query == sku:
                return product
            if cleaned_query == combined_title_sku:
                return product
            if character_name and cleaned_query == character_name:
                return product
            if combined_character_sku and cleaned_query == combined_character_sku:
                return product

        return None