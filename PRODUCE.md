# Nutrition AI Current Build

## Project Purpose

Nutrition AI is a one-week AI Engineer portfolio MVP.

The app lets an anonymous user enter meal text, retrieves the closest known food record, stores a calorie prediction, accepts user feedback, and calculates metrics from stored database records.

Current MVP scope:

- Text-only meal input
- No auth
- No user profile
- PostgreSQL storage with pgvector enabled
- Food knowledge table with optional embeddings
- Gemini embedding provider for retrieval
- Feedback linked to prediction
- Metrics calculated from saved predictions and feedback

## Current Status Snapshot

The project has moved beyond the older mock-provider-only design.

Current backend prediction flow:

```text
meal text
-> GeminiEmbeddingProvider.embed_query()
-> pgvector cosine similarity search on food_knowledge.embedding
-> Prediction database record
```

There is no current `MockAIProvider` source file in the working tree. `backend/app/providers/base.py` and `backend/app/providers/mock.py` are deleted in the current git status, while `backend/app/providers/embedding.py` and `backend/app/providers/gemini_embedding.py` are present.

The configured provider label is currently `dev`:

- `backend/app/core/config.py` default: `ai_provider = "dev"`
- `docker-compose.yml` backend environment: `AI_PROVIDER: dev`

The frontend displays `Dev provider` in `frontend/src/App.jsx`, which matches the current backend provider label.

## User Flow

1. User enters meal text in the frontend.
2. Frontend sends the text to `POST /api/predictions`.
3. Backend creates an in-memory `Prediction` object with `pending` status.
4. `PredictionService` calls `RetrievalService.find_best_food()`.
5. `RetrievalService` embeds the request text with Gemini.
6. Backend searches `food_knowledge.embedding` using pgvector cosine distance.
7. If the best match passes the similarity threshold, backend stores a successful prediction.
8. If retrieval fails or no match is returned, backend stores a failed prediction with an error message when an exception occurs.
9. Frontend displays food, calories, confidence, latency, and status.
10. User can mark the result correct or submit corrected food/calories.
11. Backend stores feedback linked to the prediction.
12. Metrics dashboard reads stored records and displays summary metrics.

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
- `backend/app/services/embedding_service.py` currently exists but is empty.

Providers:

- `backend/app/providers/embedding.py`
- `backend/app/providers/gemini_embedding.py`

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
- `backend/app/db/base.py`
- `backend/alembic/versions/0001_initial_schema.py`
- `backend/alembic/versions/f4cc016985ad_add_embedding_to_food_knowledge.py`
- `backend/alembic/versions/b94f48486ceb_expand_food_knowledge_for_embeddings.py`

Scripts:

- `backend/app/scripts/import_food_knowledge.py`
- `backend/app/scripts/seed_food_embeddings.py`
- `backend/app/scripts/test_gemini_embedding.py`
- `backend/app/scripts/test_retrieval_food.py`

## Frontend Structure

Main frontend entry:

- `frontend/src/App.jsx`
- `frontend/src/main.jsx`

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

Success response shape:

```json
{
  "id": 1,
  "request_id": "uuid",
  "predicted_food": "egg",
  "confidence": 0.82,
  "estimated_calories": 78,
  "latency_ms": 120,
  "ai_provider": "dev",
  "status": "success",
  "error_message": null
}
```

Failure response shape stored in the database:

```json
{
  "id": 2,
  "request_id": "uuid",
  "predicted_food": "unknown",
  "confidence": 0.0,
  "estimated_calories": 0,
  "latency_ms": 120,
  "ai_provider": "dev",
  "status": "failed",
  "error_message": "..."
}
```

Important current behavior:

- `PredictionService` directly assigns the single best retrieved food to the prediction.
- It does not aggregate multiple foods from one meal.
- If `RetrievalService.find_best_food()` returns `None`, the current code then tries to read `.name` from `None`, catches the exception, and stores a failed prediction.

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
  "average_latency_ms": 120.5,
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
-> RetrievalService.find_best_food()
-> RetrievedFood
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

## Retrieval Workflow

Retrieval logic lives in:

```text
backend/app/services/retrieval_service.py
```

Current flow:

```text
clean request text
-> GeminiEmbeddingProvider.embed_query()
-> FoodKnowledge.embedding.cosine_distance(query_embedding)
-> lowest-distance food record
-> similarity_score = 1 - distance
-> threshold check
-> RetrievedFood
```

Default retrieval settings:

- `gemini_embedding_model`: `gemini-embedding-001`
- `embedding_dimension`: `3072`
- `retrieval_similarity_threshold`: `0.70`

`RetrievedFood` contains:

- `food_id`
- `name`
- `food_group`
- `calories`
- `similarity_score`
- `retrieval_method`, defaulting to `pgvector_similarity`

## Embeddings

Embedding provider:

```text
backend/app/providers/gemini_embedding.py
```

The provider uses:

```python
from google import genai
from google.genai import types
```

Methods:

- `embed_query(text)` uses `RETRIEVAL_QUERY`
- `embed_document(text)` uses `RETRIEVAL_DOCUMENT`

Required environment:

- `GEMINI_API_KEY`
- optional `GEMINI_EMBEDDING_MODEL`
- optional `EMBEDDING_DIMENSION`
- optional `RETRIEVAL_SIMILARITY_THRESHOLD`

`backend/app/core/config.py` currently declares `gemini_api_key` without a default, so backend startup requires this value even in local development.

## Food Knowledge

Current table:

```text
food_knowledge
```

Important fields:

- `id`
- `name`
- `food_group`
- `aliases`
- `calories`
- `embedding`
- `created_at`

Initial migration seeds a small hardcoded list:

- egg
- toast
- rice
- chicken breast
- banana
- apple
- salad
- milk

The repository also has data/import-related paths:

- `backend/app/data/food_knowledge.csv`
- `backend/app/data/short_food_knowledge.csv`
- `backend/app/data/MyFoodData-Nutrition-Facts-SpreadSheet-Release-1-4.xlsx`
- `backend/app/scripts/import_food_knowledge.py`
- `backend/app/scripts/seed_food_embeddings.py`

The `.gitignore` excludes `*.csv` and `*.xlsx`, so local data files may exist without being tracked by git.

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

Stores food calorie facts and retrieval embeddings.

Important fields:

- `name`
- `food_group`
- `aliases`
- `calories`
- `embedding`
- `created_at`

## Metrics

Metrics are calculated by:

```text
backend/app/services/metrics_service.py
```

Metrics are not hardcoded. They are calculated from stored `predictions` and `feedback` records.

Current metrics:

- Total predictions
- Successful predictions
- Failed predictions
- Average latency
- Average confidence across successful predictions with confidence values
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

Host port:

```text
5433 -> 5432
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
AI_PROVIDER=dev
```

Also reads:

```text
backend/.env
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

Local database host port:

```text
localhost:5433
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

## Current Test State

Current tests:

- `backend/tests/test_prediction_service.py`
- `backend/tests/test_feedback_service.py`
- `backend/tests/test_metrics_service.py`

Important mismatch:

- `test_prediction_service.py` still expects the old deterministic mock result for `2 eggs and toast`: `egg, toast`, `0.85`, and `173`.
- Current `PredictionService` now depends on `RetrievalService`, which depends on Gemini embeddings and pgvector behavior.
- `conftest.py` uses in-memory SQLite, which does not provide pgvector behavior.

This means prediction service tests need to be updated to inject a fake retrieval service instead of constructing the real `RetrievalService`.

Feedback and metrics tests are closer to the current service logic because they operate directly on stored SQLAlchemy records.

## Current Limitations And Known Gaps

- No actual calorie aggregation for multi-food meals.
- No quantity parsing, so `2 eggs` is not naturally counted as two eggs.
- No unit handling for grams, cups, slices, or servings.
- No fallback keyword retrieval when embeddings are missing.
- No mock embedding provider for local tests.
- No Vertex AI provider implementation in source.
- No external nutrition API.
- No auth or user profile.
- No image upload.
- `backend/app/services/embedding_service.py` is empty.
- `backend/app/scripts/test_gemini_embedding.py` imports `VertexEmbeddingProvider`, but only `GeminiEmbeddingProvider` exists.
- `backend/app/scripts/seed_food_embeddings.py` appends `aliases` where it appears to intend `food_group`.
- `FoodKnowledge.food_group` is nullable in migration but non-null/unique in the SQLAlchemy model, so model and migration constraints should be reviewed.

## Recommended Next Improvements

1. Add a fake retrieval service in `test_prediction_service.py` so prediction tests do not call Gemini or pgvector.
2. Fix `test_gemini_embedding.py` to import `GeminiEmbeddingProvider`.
3. Fix `seed_food_embeddings.py` so document text includes `food_group` correctly.
4. Align `FoodKnowledge.food_group` model constraints with the migration and intended data shape.
5. Add a local/mock embedding provider for development and tests.
6. Add a clear no-match path in `PredictionService` instead of relying on a caught `None.name` exception.
7. Add quantity parsing so `2 eggs` counts as two eggs.
8. Add better unit handling such as grams, cups, slices, and servings.
9. Add endpoint tests for API routes.
