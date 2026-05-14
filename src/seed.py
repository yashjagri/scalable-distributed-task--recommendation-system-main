import os
from app.db import SessionLocal, apply_schema_sql
from app.repositories import UserRepository, ItemRepository, RecommendationRepository, EventRepository
from app.models_domain import User, Item, Recommendation, Event


def main():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schema", "schema.sql")
    apply_schema_sql(os.path.abspath(schema_path))

    session = SessionLocal()
    try:
        user_repo = UserRepository(session)
        item_repo = ItemRepository(session)
        rec_repo = RecommendationRepository(session)
        event_repo = EventRepository(session)

        user = user_repo.create(User(id=None, email="alice@example.com"))
        item1 = item_repo.create(Item(id=None, metadata={"title": "Item A"}))
        item2 = item_repo.create(Item(id=None, metadata={"title": "Item B"}))

        recs = [
            Recommendation(user_id=user.id, item_id=item1.id, score=0.9),
            Recommendation(user_id=user.id, item_id=item2.id, score=0.7),
        ]
        rec_repo.upsert_many_for_user(user.id, recs)

        ev = Event(id=None, user_id=user.id, item_id=item1.id, event_type="click", value={"x": 1})
        event_repo.append(ev)
        print("Seed completed:", user, item1, item2)
    finally:
        session.close()


if __name__ == "__main__":
    main()


# One-time setup script that applies the schema.sql to postgres
# also opens a session and runs all four repos and inserts test data
