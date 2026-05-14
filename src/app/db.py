import os #to read env variables
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

# getenv reads the DATABASE_URL var and fallsback on the link
# engine = create_engine() is the connectino pool where you start up connections on demand. 
# SessionLocal makes a new session every time an API is called
# a session is a unit of work, tracks every object read or modified during one operation. It ensures that there are isolated workspaces and the code remains clean
# In { with open(path, "r", encoding="utf-8") as f }, path is set to schema.sql in seed.py, this allows db.py to create the tables from schema.sql in postgres

#