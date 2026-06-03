"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "food_knowledge",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("aliases", sa.Text(), nullable=False, server_default=""),
        sa.Column("calories", sa.Integer(), nullable=False),
    )
    op.create_index("ix_food_knowledge_id", "food_knowledge", ["id"])
    op.create_index("ix_food_knowledge_name", "food_knowledge", ["name"], unique=True)

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("request_text", sa.Text(), nullable=False),
        sa.Column("predicted_food", sa.String(length=255), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("estimated_calories", sa.Integer(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("ai_provider", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_predictions_id", "predictions", ["id"])
    op.create_index("ix_predictions_request_id", "predictions", ["request_id"], unique=True)
    op.create_index("ix_predictions_status", "predictions", ["status"])

    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("prediction_id", sa.Integer(), sa.ForeignKey("predictions.id"), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("corrected_food", sa.String(length=255), nullable=True),
        sa.Column("corrected_calories", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_feedback_id", "feedback", ["id"])
    op.create_index("ix_feedback_prediction_id", "feedback", ["prediction_id"])

    food_table = sa.table(
        "food_knowledge",
        sa.column("name", sa.String),
        sa.column("aliases", sa.Text),
        sa.column("calories", sa.Integer),
    )
    op.bulk_insert(
        food_table,
        [
            {"name": "egg", "aliases": "eggs,boiled egg,scrambled egg", "calories": 78},
            {"name": "toast", "aliases": "bread,sourdough,white bread", "calories": 95},
            {"name": "rice", "aliases": "white rice,brown rice", "calories": 206},
            {"name": "chicken breast", "aliases": "chicken,grilled chicken", "calories": 165},
            {"name": "banana", "aliases": "bananas", "calories": 105},
            {"name": "apple", "aliases": "apples", "calories": 95},
            {"name": "salad", "aliases": "greens,garden salad", "calories": 150},
            {"name": "milk", "aliases": "whole milk,low fat milk", "calories": 122},
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_feedback_prediction_id", table_name="feedback")
    op.drop_index("ix_feedback_id", table_name="feedback")
    op.drop_table("feedback")
    op.drop_index("ix_predictions_status", table_name="predictions")
    op.drop_index("ix_predictions_request_id", table_name="predictions")
    op.drop_index("ix_predictions_id", table_name="predictions")
    op.drop_table("predictions")
    op.drop_index("ix_food_knowledge_name", table_name="food_knowledge")
    op.drop_index("ix_food_knowledge_id", table_name="food_knowledge")
    op.drop_table("food_knowledge")
