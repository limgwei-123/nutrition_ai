from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class FoodFact:
    name: str
    calories: int


@dataclass(frozen=True)
class AIResult:
    predicted_food: str
    confidence: float
    estimated_calories: int


class AIProvider(Protocol):
    name: str

    def predict(self, request_text: str, food_facts: list[FoodFact]) -> AIResult:
        pass
