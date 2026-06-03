from pydantic import BaseModel, ConfigDict, Field


class PredictionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class PredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: str
    predicted_food: str | None
    confidence: float | None
    estimated_calories: int | None
    latency_ms: int
    ai_provider: str
    status: str
    error_message: str | None
