from sqlalchemy import delete

from app.core.database import SessionLocal
from app.models.product_alias import ProductAlias
from app.utils.text import normalize_text


ALIASES = [
    # Spider-Man
    ("людина павук", "character", "Spider-Man", None),
    ("людина павука", "character", "Spider-Man", None),
    ("спайдер мен", "character", "Spider-Man", None),
    ("spider man", "character", "Spider-Man", None),

    # exact
    ("людина павук 1241", "product", "Spider-Man 1241", 1),
    ("spider man 1241", "product", "Spider-Man 1241", 1),

    # Marvel
    ("марвел", "franchise", "Marvel", None),

    # Batman
    ("бетмен", "character", "Batman", None),

    # Iron Man
    ("залізна людина", "character", "Iron Man", None),
]
    

def seed_aliases():
    db = SessionLocal()

    db.execute(delete(ProductAlias))

    for alias, ttype, tvalue, product_id in ALIASES:
        db.add(
            ProductAlias(
                alias=alias,
                alias_normalized=normalize_text(alias),
                target_type=ttype,
                target_value=tvalue,
                product_id=product_id,
            )
        )

    db.commit()
    db.close()
    print("Aliases seeded")


if __name__ == "__main__":
    seed_aliases()