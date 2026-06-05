from app.models.feedback import Feedback
from app.models.prediction import Prediction
from app.services.metrics_service import MetricsService


def test_metrics_service_calculates_from_stored_records(db_session):
    success = Prediction(
        request_id="request-1",
        request_text="toast",
        predicted_food="toast",
        confidence=0.8,
        estimated_calories=95,
        latency_ms=10,
        ai_provider="dev",
        status="success",
    )
    failed = Prediction(
        request_id="request-2",
        request_text="",
        latency_ms=20,
        ai_provider="dev",
        status="failed",
        error_message="request text is required",
    )
    db_session.add_all([success, failed])
    db_session.commit()
    db_session.refresh(success)

    db_session.add(
        Feedback(
            prediction_id=success.id,
            is_correct=False,
            corrected_food="2 toast",
            corrected_calories=190,
        )
    )
    db_session.commit()

    metrics = MetricsService(db_session).calculate()

    assert metrics.total_predictions == 2
    assert metrics.successful_predictions == 1
    assert metrics.failed_predictions == 1
    assert metrics.average_latency_ms == 15
    assert metrics.average_confidence == 0.8
    assert metrics.feedback_count == 1
    assert metrics.positive_feedback_rate == 0
    assert metrics.average_calorie_error == 95
