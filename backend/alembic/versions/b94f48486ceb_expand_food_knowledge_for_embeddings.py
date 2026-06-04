"""expand food knowledge for embeddings

Revision ID: b94f48486ceb
Revises: f4cc016985ad
Create Date: 2026-06-04 13:52:50.749238
"""
from alembic import op
import sqlalchemy as sa


revision = 'b94f48486ceb'
down_revision = 'f4cc016985ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


    op.add_column(
        "food_knowledge",
        sa.Column("food_group", sa.String(), nullable=True),
    )

    op.add_column(
        "food_knowledge",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )



def downgrade() -> None:
    op.drop_column("food_knowledge", "created_at")
    op.drop_column("food_knowledge", "food_group")
