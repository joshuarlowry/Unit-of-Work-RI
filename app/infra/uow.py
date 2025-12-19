from __future__ import annotations

from sqlalchemy.orm import Session

from app.infra.db import SessionFactory
from app.infra.repositories import SqlAlchemyAccountRepository


class SqlAlchemyUnitOfWork:
    """
    Unit of Work:
    - opens a DB session
    - exposes repositories bound to that session
    - commits or rolls back as a single atomic unit
    """

    session: Session
    accounts: SqlAlchemyAccountRepository

    def __init__(self) -> None:
        self.session = None  # type: ignore[assignment]
        self.accounts = None  # type: ignore[assignment]

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = SessionFactory()
        self.accounts = SqlAlchemyAccountRepository(self.session)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type is not None:
                self.rollback()
        finally:
            self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

