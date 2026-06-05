from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackRead
from app.schemas.prediction import PredictionCreate, PredictionRead
from app.services.feedback_service import FeedbackService
from app.services.prediction_service import PredictionService
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("", response_model=PredictionRead)
def create_prediction(
    payload: PredictionCreate,
    db: Session = Depends(get_db),
):
    service = PredictionService(
        db=db,
        retrieval_service=RetrievalService(db),
    )
    return service.create_prediction(payload.text)


@router.post("/{prediction_id}/feedback", response_model=FeedbackRead)
def create_feedback(
    prediction_id: int,
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
):
    service = FeedbackService(db)
    return service.create_feedback(prediction_id, payload)
