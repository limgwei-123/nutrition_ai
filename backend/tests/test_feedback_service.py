from app.models.prediction import Prediction
from app.schemas.feedback import FeedbackCreate
from app.services.feedback_service import FeedbackService


def test_feedback_links_to_prediction(db_session):
    prediction = Prediction(
        request_id="request-1",
        request_text="toast",
        predicted_food="toast",
        confidence=0.75,
        estimated_calories=95,
        latency_ms=1,
        ai_provider="dev",
        status="success",
    )
    db_session.add(prediction)
    db_session.commit()
    db_session.refresh(prediction)

    service = FeedbackService(db_session)
    feedback = service.create_feedback(
        prediction.id,
        FeedbackCreate(is_correct=False, corrected_food="2 toast", corrected_calories=190),
    )

    assert feedback.prediction_id == prediction.id
    assert feedback.is_correct is False
    assert feedback.corrected_calories == 190
