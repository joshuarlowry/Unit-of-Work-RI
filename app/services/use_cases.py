from __future__ import annotations

from app.domain.account import Account
from app.domain.exceptions import AccountNotFound, InvalidTransferAmount
from app.services.ports import UnitOfWork


def create_account(uow: UnitOfWork, *, owner: str, initial_balance_cents: int = 0) -> Account:
    if initial_balance_cents < 0:
        raise InvalidTransferAmount("initial balance cannot be negative")

    with uow:
        account = Account(id=None, owner=owner, balance_cents=0)
        if initial_balance_cents:
            account.deposit(initial_balance_cents)
        uow.accounts.add(account)
        uow.commit()
        return account


def transfer_funds(
    uow: UnitOfWork, *, from_account_id: int, to_account_id: int, amount_cents: int
) -> tuple[Account, Account]:
    if from_account_id == to_account_id:
        raise InvalidTransferAmount("cannot transfer to the same account")

    with uow:
        src = uow.accounts.get(from_account_id)
        if src is None:
            raise AccountNotFound(f"account {from_account_id} not found")

        dst = uow.accounts.get(to_account_id)
        if dst is None:
            raise AccountNotFound(f"account {to_account_id} not found")

        src.withdraw(amount_cents)
        dst.deposit(amount_cents)

        uow.accounts.save(src)
        uow.accounts.save(dst)
        uow.commit()
        return src, dst


def get_account(uow: UnitOfWork, *, account_id: int) -> Account:
    with uow:
        account = uow.accounts.get(account_id)
        if account is None:
            raise AccountNotFound(f"account {account_id} not found")
        return account

