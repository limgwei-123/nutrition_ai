"""add embedding to food knowledge

Revision ID: f4cc016985ad
Revises: 0001_initial_schema
Create Date: 2026-06-04 12:08:12.561884
"""
from alembic import op
import sqlalchemy as sa


revision = 'f4cc016985ad'
down_revision = '0001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("ALTER TABLE food_knowledge ADD COLUMN IF NOT EXISTS embedding vector(3072)")


def downgrade() -> None:
    op.execute("ALTER TABLE food_knowledge DROP COLUMN IF EXISTS embedding")
