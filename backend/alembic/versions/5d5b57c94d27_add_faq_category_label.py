"""add faq category label

Revision ID: 5d5b57c94d27
Revises: b4159cd9bfd1
Create Date: 2026-04-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5d5b57c94d27"
down_revision: Union[str, Sequence[str], None] = "b4159cd9bfd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "faq_entries",
        sa.Column("category_label", sa.String(length=255), nullable=True),
    )

    op.execute("""
        UPDATE faq_entries
        SET category_label = CASE category
            WHEN 'delivery' THEN 'Доставка'
            WHEN 'payment' THEN 'Оплата'
            WHEN 'returns' THEN 'Повернення'
            WHEN 'originality' THEN 'Оригінальність'
            WHEN 'stock' THEN 'Наявність'
            WHEN 'preorder' THEN 'Передзамовлення'
            WHEN 'manager_contact' THEN 'Контакти'
            ELSE category
        END
    """)

    op.alter_column(
        "faq_entries",
        "category_label",
        existing_type=sa.String(length=255),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("faq_entries", "category_label")