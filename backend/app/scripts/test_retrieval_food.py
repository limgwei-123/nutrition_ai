from app.db.session import SessionLocal
from app.services.retrieval_service import RetrievalService

def main():
  db = SessionLocal()

  try:
    service = RetrievalService(db)

    for text in ["egg", "banana", "rice", "chicken", "unknownxyz","waffle plain frozen ready-to-heat microwave"]:
      result = service.find_best_food(text)

      print("=" * 50)
      print("Input:", text)

      if result is None:
          print("No match")
      else:
          print("Matched:", result.name)
          print("Calories:", result.calories)
          print("Food group:", result.food_group)
          print("Similarity:", result.similarity_score)
          print("Method:", result.retrieval_method)

  finally:
    db.close()

if __name__ == "__main__":
    main()