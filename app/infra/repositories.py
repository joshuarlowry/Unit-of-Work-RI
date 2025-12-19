from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.account import Account
from app.infra.orm import AccountRow


class SqlAlchemyAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, account_id: int) -> Account | None:
        row = self._session.get(AccountRow, account_id)
        if row is None:
            return None
        return Account(id=row.id, owner=row.owner, balance_cents=row.balance_cents)

    def add(self, account: Account) -> None:
        row = AccountRow(owner=account.owner, balance_cents=account.balance_cents)
        self._session.add(row)
        self._session.flush()  # assigns PK
        account.id = row.id

    def save(self, account: Account) -> None:
        if account.id is None:
            raise ValueError("cannot save an account without an id")
        row = self._session.get(AccountRow, account.id)
        if row is None:
            # If it disappeared, treat as integrity error upstream.
            raise ValueError(f"account {account.id} does not exist")
        row.owner = account.owner
        row.balance_cents = account.balance_cents

