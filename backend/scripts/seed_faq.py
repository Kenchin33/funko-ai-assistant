import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import delete

from app.core.database import SessionLocal
from app.models.faq import FAQEntry

FAQ_SEED_DATA = [
    {
        "category": "delivery",
        "category_label": "Доставка",
        "question": "Які у вас умови доставки?",
        "answer": "Відправка замовлення здійснюється протягом 3-х робочих днів з моменту оформлення замовлення на сайті.",
        "keywords": "доставка, відправка, нова пошта",
        "button_label": None,
        "button_url": "/delivery",
        "priority": 100,
        "is_active": True,
    },
    {
        "category": "payment",
        "category_label": "Оплата",
        "question": "Які у вас варіанти оплати?",
        "answer": "1. Оплата замовлення на сайті при оформленні.\n2. Накладений платіж.",
        "keywords": "оплата, накладений платіж, оплата онлайн",
        "button_label": None,
        "button_url": "/payment",
        "priority": 90,
        "is_active": True,
    },
    {
        "category": "returns",
        "category_label": "Повернення",
        "question": "У яких випадках можливе повернення замовлення?",
        "answer": "Повернення можливе протягом 14-ти робочих днів у випадку, якщо оригінальне пакування фігурки не було пошкоджено і не відкривалось.",
        "keywords": "повернення, пакування",
        "button_label": None,
        "button_url": "/return",
        "priority": 80,
        "is_active": True,
    },
    {
        "category": "originality",
        "category_label": "Оригінальність",
        "question": "Ви продаєте оригінальну продукцію?",
        "answer": "Так, ми продаємо виключно оригінальну продукцію, яку замовляємо у офіційних постачальників у США та Європі.",
        "keywords": "оригінал, постачальники, підробка",
        "button_label": None,
        "button_url": "/original",
        "priority": 85,
        "is_active": True,
    },
    {
        "category": "stock",
        "category_label": "Наявність",
        "question": "Де я можу переглянути усю актуальну наявність?",
        "answer": "Ви завжди можете зручно переглянути усю актуальну наявність на сторінці каталогу в наявності.",
        "keywords": "наявність, актуальна наявність, перегляд",
        "button_label": "Актуальна наявність",
        "button_url": "/search?availability_status=in_stock",
        "priority": 95,
        "is_active": True,
    },
    {
        "category": "preorder",
        "category_label": "Передзамовлення",
        "question": "Які умови передзамовлення?",
        "answer": "Терміни доставки передзамовлення ви завжди можете побачити на сторінці товару.\nОплата можлива як одразу при оформленні замовлення, так і накладеним платежем на пошті. Накладений платіж можливий при попередній передоплаті 20%.",
        "keywords": "передзамовлення, умови",
        "button_label": None,
        "button_url": "/preorder",
        "priority": 88,
        "is_active": True,
    },
    {
        "category": "preorder",
        "category_label": "Передзамовлення",
        "question": "Чи можу я відмовитись від передзамовлення після оформлення?",
        "answer": "Скасувати передзамовлення можливо протягом зазначеного на сторінці товару терміну. Для цього зв'яжіться з нами через будь-який зручний спосіб на сторінці контактів.\nУ випадку, якщо термін вже минув, скасування можливе лише без повернення передоплати.",
        "keywords": "передзамовлення, скасування",
        "button_label": None,
        "button_url": "/preorder",
        "priority": 87,
        "is_active": True,
    },
    {
        "category": "manager_contact",
        "category_label": "Контакти",
        "question": "Як я можу зв'язатись з вами?",
        "answer": "Ви завжди можете написати нам на пошту або в одну з наших соціальних мереж. Посилання на наші соціальні мережі є внизу на сторінках веб сайту.\nНаша пошта: funkohunter0@gmail.com",
        "keywords": "контакти, менеджер, пошта, соціальні мережі",
        "button_label": None,
        "button_url": "/contacts",
        "priority": 92,
        "is_active": True,
    },
]


def seed_faq() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(FAQEntry))

        for item in FAQ_SEED_DATA:
            faq = FAQEntry(**item)
            db.add(faq)

        db.commit()
        print(f"Seed completed. Inserted {len(FAQ_SEED_DATA)} FAQ entries.")
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_faq()