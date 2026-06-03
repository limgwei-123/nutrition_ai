# Nutrition AI

One-week AI Engineer portfolio MVP for text-based meal calorie prediction.

## Stack

- FastAPI backend
- React + Vite frontend
- PostgreSQL with pgvector
- SQLAlchemy and Alembic
- Docker Compose

## Run

```bash
docker compose up --build
```

Frontend: http://localhost:5173

Backend health: http://localhost:8000/api/health

## Backend Tests

```bash
cd backend
pytest
```
