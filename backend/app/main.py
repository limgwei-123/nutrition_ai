from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, metrics, predictions


app = FastAPI(title="Nutrition AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
