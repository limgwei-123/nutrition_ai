from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.food_knowledge import FoodKnowledge
from app.providers.base import FoodFact


DEFAULT_FOOD_FACTS = [
    FoodFact(name="egg", calories=78),
    FoodFact(name="toast", calories=95),
    FoodFact(name="rice", calories=206),
    FoodFact(name="chicken breast", calories=165),
    FoodFact(name="banana", calories=105),
    FoodFact(name="apple", calories=95),
    FoodFact(name="salad", calories=150),
    FoodFact(name="milk", calories=122),
]


class RetrievalService:
    def __init__(self, db: Session):
        self.db = db

    def find_food_facts(self, text: str) -> list[FoodFact]:
        normalized_text = text.lower()
        facts = self._load_food_facts()

        matches = []
        for fact, terms in facts:
            if any(term and term in normalized_text for term in terms):
                matches.append(fact)

        return matches

    def _load_food_facts(self) -> list[tuple[FoodFact, list[str]]]:
        rows = self.db.scalars(select(FoodKnowledge)).all()
        if not rows:
            return [(fact, [fact.name]) for fact in DEFAULT_FOOD_FACTS]

        facts = []
        for row in rows:
            terms = [row.name.lower()]
            terms.extend(alias.strip().lower() for alias in row.aliases.split(","))
            facts.append((FoodFact(name=row.name, calories=row.calories), terms))
        return facts
