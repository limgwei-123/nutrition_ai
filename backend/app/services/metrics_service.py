from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.prediction import Prediction
from app.schemas.metrics import MetricsRead


class MetricsService:
    def __init__(self, db: Session):
        self.db = db

    def calculate(self) -> MetricsRead:
        predictions = list(self.db.scalars(select(Prediction)).all())
        feedback = list(self.db.scalars(select(Feedback)).all())

        successful = [item for item in predictions if item.status == "success"]
        failed = [item for item in predictions if item.status == "failed"]
        confidence_values = [
            item.confidence for item in successful if item.confidence is not None
        ]
        calorie_errors = [
            abs(item.prediction.estimated_calories - item.corrected_calories)
            for item in feedback
            if item.corrected_calories is not None
            and item.prediction.estimated_calories is not None
        ]

        return MetricsRead(
            total_predictions=len(predictions),
            successful_predictions=len(successful),
            failed_predictions=len(failed),
            average_latency_ms=round(mean([item.latency_ms for item in predictions]), 2)
            if predictions
            else 0,
            average_confidence=round(mean(confidence_values), 2)
            if confidence_values
            else 0,
            feedback_count=len(feedback),
            positive_feedback_rate=round(
                len([item for item in feedback if item.is_correct]) / len(feedback),
                2,
            )
            if feedback
            else 0,
            average_calorie_error=round(mean(calorie_errors), 2)
            if calorie_errors
            else None,
        )
