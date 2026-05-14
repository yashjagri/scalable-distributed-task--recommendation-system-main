from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, text
from .models_db import UserORM, ItemORM, EventORM, RecommendationORM
from .models_domain import User, Item, Event, Recommendation
from .mappings import (orm_user_to_domain, domain_user_to_orm, orm_item_to_domain,
                       domain_item_to_orm, domain_event_to_orm, orm_recommendation_to_domain,
                       domain_recommendation_to_orm)


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        orm = domain_user_to_orm(user)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm_user_to_domain(orm)

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        orm = self.session.get(UserORM, user_id)
        return orm_user_to_domain(orm) if orm is not None else None


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, item: Item) -> Item:
        orm = domain_item_to_orm(item)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm_item_to_domain(orm)

    def get_by_id(self, item_id: UUID) -> Optional[Item]:
        orm = self.session.get(ItemORM, item_id)
        return orm_item_to_domain(orm) if orm is not None else None


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def append(self, event: Event) -> Event:
        orm = domain_event_to_orm(event)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return Event(id=orm.id, user_id=orm.user_id, item_id=orm.item_id,
                     event_type=orm.event_type, value=orm.value, created_at=orm.created_at)

    def delete_older_than(self, *, days: int) -> int:
        sql = text("DELETE FROM events WHERE created_at < now() - (:days || ' days')::interval")
        result = self.session.execute(sql, {"days": str(days)})
        self.session.commit()
        return result.rowcount if result is not None else 0


class RecommendationRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert_many_for_user(self, user_id: UUID, recommendations: List[Recommendation]) -> None:
        self.session.execute(delete(RecommendationORM).where(RecommendationORM.user_id == user_id))
        orm_objs = [domain_recommendation_to_orm(r) for r in recommendations]
        if orm_objs:
            self.session.bulk_save_objects(orm_objs)
        self.session.commit()

    def get_top_n_for_user(self, user_id: UUID, n: int) -> List[Recommendation]:
        stmt = (select(RecommendationORM)
                .where(RecommendationORM.user_id == user_id)
                .order_by(RecommendationORM.score.desc())
                .limit(n))
        rows = self.session.execute(stmt).scalars().all()
        return [orm_recommendation_to_domain(r) for r in rows]

# Repositories.py is the only file that talks to the db, db.py manages conneciton pool and sessions but this file has methods that talk to postgres
# We isolate all of these files so that if we were to switch dbs then the transition is easy