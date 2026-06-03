from time import perf_counter
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.providers.base import AIProvider
from app.services.retrieval_service import RetrievalService


class PredictionService:
    def __init__(
        self,
        db: Session,
        ai_provider: AIProvider,
        retrieval_service: RetrievalService,
    ):
        self.db = db
        self.ai_provider = ai_provider
        self.retrieval_service = retrieval_service

    def create_prediction(self, request_text: str) -> Prediction:
        started_at = perf_counter()
        prediction = Prediction(
            request_id=str(uuid4()),
            request_text=request_text,
            ai_provider=self.ai_provider.name,
            status="pending",
            latency_ms=0,
        )

        try:
            food_facts = self.retrieval_service.find_food_facts(request_text)
            result = self.ai_provider.predict(request_text, food_facts)
            prediction.predicted_food = result.predicted_food
            prediction.confidence = result.confidence
            prediction.estimated_calories = result.estimated_calories
            prediction.status = "success"
        except Exception as exc:
            prediction.status = "failed"
            prediction.error_message = str(exc)
        finally:
            prediction.latency_ms = int((perf_counter() - started_at) * 1000)
            self.db.add(prediction)
            self.db.commit()
            self.db.refresh(prediction)

        return prediction
