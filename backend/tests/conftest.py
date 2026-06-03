import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base
from app.models.feedback import Feedback
from app.models.food_knowledge import FoodKnowledge
from app.models.prediction import Prediction


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Feedback", "FoodKnowledge", "Prediction"]
