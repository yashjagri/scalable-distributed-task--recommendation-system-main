from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func

Base = declarative_base()
# creates a special parent class, every ORM class inherits from Base (the class that makes ORM mapping work)

class UserORM(Base):#sqlalchemy sees the Base class and knows that UserORM is part of the table mapping and keeps an internal registry of tables
    __tablename__ = "users" #__tablename__ helps sqlalchemy to understand what class this maps to (sql schema)
    id         = Column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    email      = Column(Text, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class ItemORM(Base):
    __tablename__ = "items"
    id         = Column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    metadata   = Column(JSONB, nullable=False, server_default="'{}'")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class EventORM(Base):
    __tablename__ = "events"
    id         = Column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id    = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id    = Column(PG_UUID(as_uuid=True), ForeignKey("items.id", ondelete="SET NULL"), nullable=True)
    event_type = Column(Text, nullable=False)
    value      = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class RecommendationORM(Base):
    __tablename__ = "recommendations"
    user_id    = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    item_id    = Column(PG_UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    score      = Column(Float, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


# this whole thing is taking all of these classes and mapping them relationally whilst also connecting them to the postgres
# all classes inherit the declarative_base / Base class which establishes the mappings
# all of the column descriptions are exactly like the sql schema except written in python