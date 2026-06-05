from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.food_knowledge import FoodKnowledge
from app.providers.gemini_embedding import GeminiEmbeddingProvider

@dataclass
class RetrievedFood:
    food_id: int
    name: str
    food_group: str | None
    calories: int
    similarity_score: float
    retrieval_method: str = "pgvector_similarity"

class RetrievalService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_provider = GeminiEmbeddingProvider(
            api_key=settings.gemini_api_key,
            model = settings.gemini_embedding_model
        )
        self.threshold = settings.retrieval_similarity_threshold

    def find_best_food(self, text: str) -> RetrievedFood | None:
        cleaned_text = text.strip().lower()

        if not cleaned_text:
            return None

        query_embedding = self.embedding_provider.embed_query(cleaned_text)

        distance_expr = FoodKnowledge.embedding.cosine_distance(query_embedding)

        stmt = (
            select(FoodKnowledge, distance_expr.label("distance"))
            .where(FoodKnowledge.embedding.is_not(None))
            .order_by(distance_expr)
            .limit(1)
        )

        result = self.db.execute(stmt).first()

        if result is None:
            return None

        food, distance = result

        similarity_score = 1 - float(distance)

        if similarity_score < self.threshold:
            return None

        return RetrievedFood(
            food_id=food.id,
            name = food.name,
            food_group=getattr(food, "food_group", None),
            calories=food.calories,
            similarity_score=similarity_score
        )