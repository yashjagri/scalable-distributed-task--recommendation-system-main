import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models_db import Base
from app.models_domain import User, Item, Recommendation, Event
from app.repositories import UserRepository, ItemRepository, RecommendationRepository, EventRepository

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/reccore"

engine = create_engine(DATABASE_URL, future=True)
TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_top_n_ordering():
    session = TestSession()
    user_repo = UserRepository(session)
    item_repo = ItemRepository(session)
    rec_repo = RecommendationRepository(session)

    user = user_repo.create(User(id=None, email="test@example.com"))
    items = [item_repo.create(Item(id=None, metadata={"title": f"Item {i}"})) for i in range(5)]

    recs = [Recommendation(user_id=user.id, item_id=items[i].id, score=float(i)) for i in range(5)]
    rec_repo.upsert_many_for_user(user.id, recs)

    top3 = rec_repo.get_top_n_for_user(user.id, 3)
    assert len(top3) == 3
    assert top3[0].score > top3[1].score > top3[2].score
    session.close()


def test_delete_older_than():
    from sqlalchemy import text
    session = TestSession()
    user_repo = UserRepository(session)
    item_repo = ItemRepository(session)
    event_repo = EventRepository(session)

    user = user_repo.create(User(id=None, email="test2@example.com"))
    item = item_repo.create(Item(id=None, metadata={}))

    event_repo.append(Event(id=None, user_id=user.id, item_id=item.id, event_type="click"))
    session.execute(text("UPDATE events SET created_at = now() - interval '60 days'"))
    session.commit()

    event_repo.append(Event(id=None, user_id=user.id, item_id=item.id, event_type="click"))

    deleted = event_repo.delete_older_than(days=30)
    assert deleted == 1
    session.close()
