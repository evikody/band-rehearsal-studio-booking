"""seed the single studio row

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-09

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

# Lightweight table reference for the insert -- not the full ORM model.
# This keeps the migration self-contained and correct even if the
# Studio model's Python definition changes in the future.
studios = sa.table(
    "studios",
    sa.column("name", sa.String),
    sa.column("description", sa.String),
    sa.column("price_per_hour", sa.Numeric),
)


def upgrade() -> None:
    op.bulk_insert(
        studios,
        [
            {
                "name": "Main Rehearsal Room",
                "description": "Placeholder -- edit via PUT /api/studios",
                "price_per_hour": 20.00,
            }
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM studios")
