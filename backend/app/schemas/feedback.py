from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    is_correct: bool
    corrected_food: str | None = Field(default=None, max_length=255)
    corrected_calories: int | None = Field(default=None, ge=0)


class FeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prediction_id: int
    is_correct: bool
    corrected_food: str | None
    corrected_calories: int | None
