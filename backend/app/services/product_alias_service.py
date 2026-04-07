from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product_alias import ProductAlias
from app.utils.text import normalize_text


class ProductAliasService:
    @staticmethod
    def find_alias_matches(db: Session, text: str) -> list[ProductAlias]:
        normalized = normalize_text(text)

        stmt = select(ProductAlias).where(ProductAlias.is_active.is_(True))
        aliases = list(db.scalars(stmt).all())

        matched = []

        for alias in aliases:
            if alias.alias_normalized in normalized:
                matched.append(alias)

        return matched