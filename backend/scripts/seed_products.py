from decimal import Decimal

from sqlalchemy import delete

from app.core.database import SessionLocal
from app.models.product import Product

PRODUCTS_SEED_DATA = [
    {
        "title": "Funko Pop! Spider-Man 1241",
        "slug": "funko-pop-spider-man-1241",
        "sku": "1241",
        "url": "/products/funko-pop-spider-man-1241",
        "description": "Колекційна фігурка Spider-Man у вініловому виконанні.",
        "price": Decimal("799.00"),
        "image_url": "/images/products/spider-man-1241.jpg",
        "brand": "Funko",
        "series": "Marvel",
        "character_name": "Spider-Man",
        "franchise": "Marvel",
        "in_stock": True,
        "is_active": True,
    },
    {
        "title": "Funko Pop! Miles Morales 1092",
        "slug": "funko-pop-miles-morales-1092",
        "sku": "1092",
        "url": "/products/funko-pop-miles-morales-1092",
        "description": "Фігурка Miles Morales із всесвіту Marvel.",
        "price": Decimal("759.00"),
        "image_url": "/images/products/miles-morales-1092.jpg",
        "brand": "Funko",
        "series": "Marvel",
        "character_name": "Miles Morales",
        "franchise": "Marvel",
        "in_stock": True,
        "is_active": True,
    },
    {
        "title": "Funko Pop! Spider-Gwen 1224",
        "slug": "funko-pop-spider-gwen-1224",
        "sku": "1224",
        "url": "/products/funko-pop-spider-gwen-1224",
        "description": "Колекційна фігурка Spider-Gwen.",
        "price": Decimal("789.00"),
        "image_url": "/images/products/spider-gwen-1224.jpg",
        "brand": "Funko",
        "series": "Marvel",
        "character_name": "Spider-Gwen",
        "franchise": "Marvel",
        "in_stock": False,
        "is_active": True,
    },
    {
        "title": "Funko Pop! Iron Man 285",
        "slug": "funko-pop-iron-man-285",
        "sku": "285",
        "url": "/products/funko-pop-iron-man-285",
        "description": "Фігурка Iron Man для фанатів Marvel.",
        "price": Decimal("699.00"),
        "image_url": "/images/products/iron-man-285.jpg",
        "brand": "Funko",
        "series": "Marvel",
        "character_name": "Iron Man",
        "franchise": "Marvel",
        "in_stock": True,
        "is_active": True,
    },
    {
        "title": "Funko Pop! Batman 01",
        "slug": "funko-pop-batman-01",
        "sku": "01",
        "url": "/products/funko-pop-batman-01",
        "description": "Класична фігурка Batman.",
        "price": Decimal("649.00"),
        "image_url": "/images/products/batman-01.jpg",
        "brand": "Funko",
        "series": "DC",
        "character_name": "Batman",
        "franchise": "DC",
        "in_stock": True,
        "is_active": True,
    },
]


def seed_products() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(Product))

        for item in PRODUCTS_SEED_DATA:
            product = Product(**item)
            db.add(product)

        db.commit()
        print(f"Seed completed. Inserted {len(PRODUCTS_SEED_DATA)} products.")
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_products()