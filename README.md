# Nutrition AI

Nutrition AI is a one-week AI Engineer portfolio project for text-based meal calorie prediction.

The app lets a user describe a meal in plain English, retrieves the closest matching food knowledge record, stores the prediction result, accepts user feedback, and calculates product metrics from saved database records.

## Demo

- YouTube demo: https://youtu.be/_R1zZcrbVz8
- Live app demo: Current System still under development

## What This Project Shows

- Full-stack MVP development with FastAPI and React.
- PostgreSQL data modeling with SQLAlchemy and Alembic migrations.
- pgvector-backed semantic food retrieval.
- Gemini embedding integration for query and food-document embeddings.
- Service-based backend architecture with thin API routers.
- Stored prediction, feedback, and metrics workflows.
- Docker Compose setup for local development.

## Core User Flow

1. The user enters a meal description.
2. The frontend sends the text to the FastAPI backend.
3. The backend embeds the request text.
4. The retrieval service searches food knowledge records with pgvector cosine similarity.
5. The prediction is stored with confidence, calories, latency, provider, and status.
6. The user can submit feedback if the prediction is correct or wrong.
7. The metrics panel updates from stored prediction and feedback records.

## Tech Stack

- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL + pgvector
- ORM: SQLAlchemy
- Migrations: Alembic
- Embeddings: Gemini embedding API
- Container: Docker Compose
- Tests: pytest

## Features

- Text-based meal calorie estimation.
- Semantic retrieval from food knowledge records.
- Prediction persistence with operational metadata.
- Feedback linked to a specific prediction.
- Metrics calculated from stored database records.
- Responsive React UI for predictions, feedback, and metrics.

## API Overview

- `GET /api/health` checks backend health.
- `POST /api/predictions` creates a meal calorie prediction.
- `POST /api/predictions/{prediction_id}/feedback` records user feedback.
- `GET /api/metrics` returns stored prediction and feedback metrics.

## Project Structure

```text
backend/
  app/
    models/       SQLAlchemy models
    providers/    embedding providers
    routers/      FastAPI route definitions
    schemas/      Pydantic request/response schemas
    services/     business logic
  alembic/        database migrations
  tests/          pytest service tests

frontend/
  src/
    components/   React UI components
    api.js        frontend API client
    App.jsx       main app shell
```

## Local Setup

Create a backend environment file:

```text
backend/.env
```

Required value:

```text
GEMINI_API_KEY=your_api_key_here
```

Then run the app:

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

Database:

```text
localhost:5433
```

## Running Tests

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

- The current MVP predicts one best-matching food record rather than a full multi-item meal breakdown.
- Quantity parsing is not implemented yet, so inputs such as `2 eggs` are not counted as two servings.
- Unit handling for grams, cups, slices, and servings is not implemented yet.
- A mock embedding provider would make local tests and development easier.
- No authentication, user profile, external nutrition API, or image upload is included.

## Future Improvements

- Add quantity and serving-size parsing.
- Support multi-food meal aggregation.
- Add a local mock embedding provider for tests.
- Improve no-match handling and fallback retrieval.
- Add endpoint-level API tests.
- Deploy the frontend and backend for a public live demo.
