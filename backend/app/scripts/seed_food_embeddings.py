from app.core.config import settings
from app.db.session import SessionLocal
from app.models.food_knowledge import FoodKnowledge
from app.providers.gemini_embedding import GeminiEmbeddingProvider

def build_food_document(food: FoodKnowledge) -> str:
  parts = [food.name]

  if getattr(food, "aliases", None):
    parts.append(str(food.aliases))

  if getattr(food, "food_group", None):
    parts.append(str(food.aliases))

  return " ".join(part for part in parts if part)

def main(force: bool = False):
  db = SessionLocal()

  provider = GeminiEmbeddingProvider(
    api_key=settings.gemini_api_key,
    model=settings.gemini_embedding_model,
  )

  updated = 0
  skipped = 0

  try:
    foods = db.query(FoodKnowledge).all()

    for food in foods:
      if food.embedding is not None and not force:
        skipped +=1
        continue

      document_text = build_food_document(food)
      embedding = provider.embed_document(document_text)

      if len(embedding) != settings.embedding_dimension:
        raise ValueError(
           f"Unexpected embedding length for {food.name}: "
           f"{len(embedding)}"
        )

      food.embedding = embedding
      updated +=1

    db.commit()

    print(f"Updated embeddings: {updated}")
    print(f"Skipped existing embeddings: {skipped}")

  except Exception:
    db.rollback()
    raise

  finally:
    db.close()

if __name__ == "__main__":
    main()


