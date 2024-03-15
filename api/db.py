import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api.models.base import Base

engine = None


def init_db():
    global engine

    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db_name}",
        echo=True,
        pool_size=20,
    )

    Base.metadata.create_all(engine)


def get_session():
    return Session(engine)
