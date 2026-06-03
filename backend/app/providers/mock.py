from app.providers.base import AIProvider, AIResult, FoodFact


class MockAIProvider(AIProvider):
    name = "mock"

    def predict(self, request_text: str, food_facts: list[FoodFact]) -> AIResult:
        if not request_text.strip():
            raise ValueError("request text is required")

        if not food_facts:
            return AIResult(
                predicted_food=request_text.strip(),
                confidence=0.35,
                estimated_calories=500,
            )

        estimated_calories = sum(item.calories for item in food_facts)
        predicted_food = ", ".join(item.name for item in food_facts)
        confidence = min(0.95, 0.65 + (len(food_facts) * 0.1))

        return AIResult(
            predicted_food=predicted_food,
            confidence=round(confidence, 2),
            estimated_calories=estimated_calories,
        )
