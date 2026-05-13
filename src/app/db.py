import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .models_db import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/reccore")

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_tables_from_orm():
    Base.metadata.create_all(bind=engine)


def apply_schema_sql(path: str):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

