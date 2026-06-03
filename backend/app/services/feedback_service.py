from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.prediction import Prediction
from app.schemas.feedback import FeedbackCreate


class FeedbackService:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, prediction_id: int, payload: FeedbackCreate) -> Feedback:
        prediction = self.db.get(Prediction, prediction_id)
        if prediction is None:
            raise HTTPException(status_code=404, detail="Prediction not found")

        feedback = Feedback(
            prediction_id=prediction_id,
            is_correct=payload.is_correct,
            corrected_food=payload.corrected_food,
            corrected_calories=payload.corrected_calories,
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
