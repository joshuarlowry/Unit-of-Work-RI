from __future__ import annotations

from typing import Protocol

from app.domain.account import Account


class AccountRepository(Protocol):
    def get(self, account_id: int) -> Account | None: ...

    def add(self, account: Account) -> None: ...

    def save(self, account: Account) -> None: ...


class UnitOfWork(Protocol):
    accounts: AccountRepository

    def __enter__(self) -> "UnitOfWork": ...

    def __exit__(self, exc_type, exc, tb) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...

