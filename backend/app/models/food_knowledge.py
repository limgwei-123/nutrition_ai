from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class FoodKnowledge(Base):
    __tablename__ = "food_knowledge"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    aliases: Mapped[str] = mapped_column(Text, default="")
    calories: Mapped[int] = mapped_column(Integer)
