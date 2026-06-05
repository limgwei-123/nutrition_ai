from time import perf_counter
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.services.retrieval_service import RetrievalService
from app.core.config import settings

class PredictionService:
    def __init__(
        self,
        db: Session,
        retrieval_service: RetrievalService,
    ):
        self.db = db
        self.retrieval_service = retrieval_service
        self.ai_provider = settings.ai_provider

    def create_prediction(self, request_text: str) -> Prediction:
        started_at = perf_counter()
        request_id = str(uuid4())

        prediction = Prediction(
            request_id=request_id,
            request_text=request_text,
            predicted_food="unknown",
            confidence=0.0,
            ai_provider=self.ai_provider,
            estimated_calories=0,
            status="pending",
            latency_ms=0,
            error_message=None,
        )

        try:
            retrieved_food  = self.retrieval_service.find_best_food(request_text)

            prediction.predicted_food = retrieved_food.name
            prediction.estimated_calories = retrieved_food.calories
            prediction.confidence = retrieved_food.similarity_score
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
