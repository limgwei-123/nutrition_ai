# Nutrition AI Current Build

## Project Purpose

Nutrition AI is a one-week AI Engineer portfolio MVP.

The app lets an anonymous user enter meal text, predicts a simple calorie estimate, records the prediction, accepts user feedback, and calculates metrics from stored database records.

Current MVP scope:

- Text-only meal input
- No auth
- No user profile
- Static food knowledge
- Mock AI provider
- PostgreSQL storage
- Feedback linked to prediction
- Metrics calculated from saved predictions and feedback

## User Flow

1. User enters meal text in the frontend.
2. Frontend sends the text to `POST /api/predictions`.
3. Backend creates a prediction request record.
4. Backend retrieves matching static food facts.
5. `MockAIProvider` converts those facts into a prediction result.
6. Backend stores the prediction in PostgreSQL.
7. Frontend displays predicted food, calories, confidence, latency, and status.
8. User can mark the result correct or submit corrected food/calories.
9. Backend stores feedback linked to the prediction.
10. Metrics dashboard reads stored records and displays summary metrics.

## Backend Structure

Main backend entry:

- `backend/app/main.py`

Routers:

- `backend/app/routers/health.py`
- `backend/app/routers/predictions.py`
- `backend/app/routers/metrics.py`

Services:

- `backend/app/services/prediction_service.py`
- `backend/app/services/retrieval_service.py`
- `backend/app/services/feedback_service.py`
- `backend/app/services/metrics_service.py`

Providers:

- `backend/app/providers/base.py`
- `backend/app/providers/mock.py`

Models:

- `backend/app/models/prediction.py`
- `backend/app/models/feedback.py`
- `backend/app/models/food_knowledge.py`

Schemas:

- `backend/app/schemas/prediction.py`
- `backend/app/schemas/feedback.py`
- `backend/app/schemas/metrics.py`

Database and migrations:

- `backend/app/db/session.py`
- `backend/alembic/versions/0001_initial_schema.py`

## Frontend Structure

Main frontend entry:

- `frontend/src/App.jsx`

API client:

- `frontend/src/api.js`

Components:

- `frontend/src/components/PredictionForm.jsx`
- `frontend/src/components/PredictionResult.jsx`
- `frontend/src/components/FeedbackPanel.jsx`
- `frontend/src/components/MetricsPanel.jsx`

Styles:

- `frontend/src/styles.css`

Vite config:

- `frontend/vite.config.mjs`

## API Endpoints

### `GET /api/health`

Checks whether the backend is running.

Response:

```json
{
  "status": "ok"
}
```

### `POST /api/predictions`

Creates a calorie prediction from meal text.

Request:

```json
{
  "text": "2 eggs and toast"
}
```

Response example:

```json
{
  "id": 1,
  "request_id": "uuid",
  "predicted_food": "egg, toast",
  "confidence": 0.85,
  "estimated_calories": 173,
  "latency_ms": 1,
  "ai_provider": "mock",
  "status": "success",
  "error_message": null
}
```

### `POST /api/predictions/{prediction_id}/feedback`

Records user feedback for a prediction.

Request when correct:

```json
{
  "is_correct": true
}
```

Request when wrong:

```json
{
  "is_correct": false,
  "corrected_food": "2 scrambled eggs and 1 slice toast",
  "corrected_calories": 410
}
```

### `GET /api/metrics`

Returns metrics calculated from stored database records.

Response example:

```json
{
  "total_predictions": 10,
  "successful_predictions": 9,
  "failed_predictions": 1,
  "average_latency_ms": 2.5,
  "average_confidence": 0.8,
  "feedback_count": 4,
  "positive_feedback_rate": 0.75,
  "average_calorie_error": 95
}
```

## Prediction Workflow

The main prediction workflow lives in:

```text
backend/app/services/prediction_service.py
```

Current flow:

```text
request text
-> RetrievalService.find_food_facts()
-> MockAIProvider.predict()
-> Prediction database record
```

The prediction workflow records:

- `request_id`
- `request_text`
- `predicted_food`
- `confidence`
- `estimated_calories`
- `latency_ms`
- `ai_provider`
- `status`
- `error_message`

This matches the project rule that predictions must be stored with operational metadata.

## What Is Mocked

### AI Provider Is Mocked

Current provider:

```text
backend/app/providers/mock.py
```

The app does not call Vertex AI, OpenAI, or any external model yet.

`MockAIProvider` creates deterministic output from retrieved food facts.

If matched food facts exist:

```python
estimated_calories = sum(item.calories for item in food_facts)
predicted_food = ", ".join(item.name for item in food_facts)
confidence = min(0.95, 0.65 + (len(food_facts) * 0.1))
```

Example:

```text
Input: 2 eggs and toast
Matched facts: egg, toast
Calories: 78 + 95 = 173
Confidence: 0.65 + 2 * 0.1 = 0.85
```

Result:

```json
{
  "predicted_food": "egg, toast",
  "confidence": 0.85,
  "estimated_calories": 173
}
```

If no food facts match, it returns a generic fallback:

```json
{
  "predicted_food": "original user text",
  "confidence": 0.35,
  "estimated_calories": 500
}
```

### Food Knowledge Is Static

Current retrieval source:

```text
backend/app/services/retrieval_service.py
```

The system uses static food facts such as:

- egg: 78 calories
- toast: 95 calories
- rice: 206 calories
- chicken breast: 165 calories
- banana: 105 calories
- apple: 95 calories
- salad: 150 calories
- milk: 122 calories

The Alembic migration also seeds these into the database:

```text
backend/alembic/versions/0001_initial_schema.py
```

If the database table has records, retrieval uses those records.

If the table is empty, retrieval falls back to the hardcoded `DEFAULT_FOOD_FACTS`.

### No Real RAG Yet

The project uses a RAG-ready shape, but it is not true vector retrieval yet.

Current:

```text
keyword matching against static food facts
```

Future:

```text
embedding -> pgvector similarity search -> retrieved food context -> AI provider
```

The project already uses a pgvector Docker image and creates the `vector` extension in the initial migration, but no embedding column or vector search is implemented yet.

## FoodFact vs AIResult

`FoodFact` means retrieved knowledge.

Defined in:

```text
backend/app/providers/base.py
```

Example:

```python
FoodFact(name="egg", calories=78)
```

It answers:

```text
What food knowledge did the system find?
```

`AIResult` means final prediction output.

Example:

```python
AIResult(
    predicted_food="egg, toast",
    confidence=0.85,
    estimated_calories=173,
)
```

It answers:

```text
What result should the user see and what should be stored?
```

Simple distinction:

```text
FoodFact = evidence / retrieved knowledge
AIResult = final prediction answer
```

## Database Tables

### `predictions`

Stores every prediction attempt.

Important fields:

- `request_id`
- `request_text`
- `predicted_food`
- `confidence`
- `estimated_calories`
- `latency_ms`
- `ai_provider`
- `status`
- `error_message`
- `created_at`

### `feedback`

Stores user feedback linked to a prediction.

Important fields:

- `prediction_id`
- `is_correct`
- `corrected_food`
- `corrected_calories`
- `created_at`

### `food_knowledge`

Stores static food calorie facts.

Important fields:

- `name`
- `aliases`
- `calories`

## Metrics

Metrics are calculated by:

```text
backend/app/services/metrics_service.py
```

Metrics are not hardcoded.

They are calculated from stored `predictions` and `feedback` records.

Current metrics:

- Total predictions
- Successful predictions
- Failed predictions
- Average latency
- Average confidence
- Feedback count
- Positive feedback rate
- Average calorie error when corrected calories exist

## Docker Compose

Compose services:

### `db`

Uses:

```text
pgvector/pgvector:pg16
```

Database:

```text
nutrition_ai
```

### `backend`

Runs:

```bash
alembic upgrade head &&
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Environment:

```text
DATABASE_URL=postgresql+psycopg://nutrition:nutrition@db:5432/nutrition_ai
AI_PROVIDER=mock
```

### `frontend`

Runs:

```bash
npm run dev
```

Uses:

```text
VITE_API_BASE_URL=http://localhost:8000/api
```

## Run The Project

From the project root:

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend health:

```text
http://localhost:8000/api/health
```

## Run Tests

Backend tests:

```bash
cd backend
python -m pytest
```

Frontend build:

```bash
cd frontend
npm install
npm run build
```

## Current Limitations

- No real AI call yet.
- No Vertex AI provider enabled.
- No external nutrition API.
- No real embedding generation.
- No pgvector similarity search yet.
- No quantity parsing yet, so `2 eggs` currently matches `egg` once.
- No auth or user profile.
- No image upload.

## Recommended Next Improvements

1. Add quantity parsing so `2 eggs` counts as two eggs.
2. Add better unit handling such as grams, cups, slices, and servings.
3. Add an embedding column to `food_knowledge`.
4. Implement pgvector similarity search.
5. Add a real provider behind `AIProvider`, only when explicitly needed.
6. Add endpoint tests for API routes.
7. Add frontend loading and error state tests if the UI grows.
