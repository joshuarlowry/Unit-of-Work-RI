from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import database_url


def build_engine():
    url = database_url()
    # SQLite needs check_same_thread=False when using threads (FastAPI)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite:") else {}
    return create_engine(url, future=True, echo=False, connect_args=connect_args)


ENGINE = build_engine()
SessionFactory = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)

