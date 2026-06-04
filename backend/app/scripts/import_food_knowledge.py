import csv
from pathlib import Path

from app.db.session import SessionLocal
from app.models.food_knowledge import FoodKnowledge

CSV_PATH = Path("app/data/short_food_knowledge.csv")

def main():
  db = SessionLocal()

  created = 0
  updated = 0

  try:
    with CSV_PATH.open("r", encoding="utf-8-sig") as file:
      reader = csv.DictReader(file)

      for row in reader:
        name = row["name"].strip().lower()
        food_group = row["food_group"].strip().lower()
        calories = int(row["calories"])

        existing = (
          db.query(FoodKnowledge).filter(FoodKnowledge.name == name).first()
        )

        if existing:
          existing.food_group = food_group
          existing.calories = calories
          existing.embedding = None
          updated +=1
        else:
          food = FoodKnowledge(
            name=name,
            aliases=None,
            food_group=food_group,
            calories=calories,
            embedding=None,
          )

          db.add(food)
          created += 1

    db.commit()

    print(f"Created: {created}")
    print(f"Updated: {updated}")

  finally:
    db.close()

if __name__ == "__main__":
  main()