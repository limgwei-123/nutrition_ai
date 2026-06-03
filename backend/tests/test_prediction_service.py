from app.providers.mock import MockAIProvider
from app.services.prediction_service import PredictionService
from app.services.retrieval_service import RetrievalService


def test_prediction_service_records_success(db_session):
    service = PredictionService(
        db=db_session,
        ai_provider=MockAIProvider(),
        retrieval_service=RetrievalService(db_session),
    )

    prediction = service.create_prediction("2 eggs and toast")

    assert prediction.request_id
    assert prediction.predicted_food == "egg, toast"
    assert prediction.confidence == 0.85
    assert prediction.estimated_calories == 173
    assert prediction.ai_provider == "mock"
    assert prediction.status == "success"
    assert prediction.error_message is None
