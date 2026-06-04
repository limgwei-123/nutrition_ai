from sqlalchemy import DateTime,Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from datetime import UTC, datetime

from app.db.session import Base


class FoodKnowledge(Base):
    __tablename__ = "food_knowledge"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    food_group: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    aliases: Mapped[str] = mapped_column(Text, default="")
    calories: Mapped[int] = mapped_column(Integer)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(3072), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
