# Nutrition AI Project Instructions

This project is a one-week AI Engineer portfolio project.

## Stack

- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL + pgvector
- ORM: SQLAlchemy
- Migrations: Alembic
- Container: Docker Compose

## Important Architecture Rules

- Routers should stay thin.
- Business logic belongs in services.
- AI calls must go through AIProvider.
- Use MockAIProvider for local development.
- Use VertexAIProvider only when explicitly requested.
- Prediction workflow must record:
  - request_id
  - predicted_food
  - confidence
  - estimated_calories
  - latency_ms
  - ai_provider
  - status
  - error_message if failed
- Feedback must link to prediction.
- Metrics must be calculated from stored database records.

## Testing Rules

- Add tests for service logic when possible.
- Do not skip tests for MetricsService.
- Keep tests simple and maintainable.

## Coding Style

- Prefer simple code over clever abstractions.
- Do not rewrite unrelated files.
- Do not introduce unnecessary frameworks.
- Keep the MVP small.