"""rename studios table to studio

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-10

"""
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("studios", "studio")


def downgrade() -> None:
    op.rename_table("studio", "studios")