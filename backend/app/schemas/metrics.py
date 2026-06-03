from pydantic import BaseModel


class MetricsRead(BaseModel):
    total_predictions: int
    successful_predictions: int
    failed_predictions: int
    average_latency_ms: float
    average_confidence: float
    feedback_count: int
    positive_feedback_rate: float
    average_calorie_error: float | None
