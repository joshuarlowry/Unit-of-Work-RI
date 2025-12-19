from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.schemas import AccountCreate, AccountRead, TransferCreate, TransferResult
from app.infra.uow import SqlAlchemyUnitOfWork
from app.services.use_cases import create_account, get_account, transfer_funds

router = APIRouter()


def uow_dep() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/accounts", response_model=AccountRead, status_code=201)
def post_account(payload: AccountCreate, uow: SqlAlchemyUnitOfWork = Depends(uow_dep)) -> AccountRead:
    account = create_account(uow, owner=payload.owner, initial_balance_cents=payload.initial_balance_cents)
    assert account.id is not None
    return AccountRead(id=account.id, owner=account.owner, balance_cents=account.balance_cents)


@router.get("/accounts/{account_id}", response_model=AccountRead)
def get_account_by_id(account_id: int, uow: SqlAlchemyUnitOfWork = Depends(uow_dep)) -> AccountRead:
    account = get_account(uow, account_id=account_id)
    assert account.id is not None
    return AccountRead(id=account.id, owner=account.owner, balance_cents=account.balance_cents)


@router.post("/transfers", response_model=TransferResult, status_code=201)
def post_transfer(payload: TransferCreate, uow: SqlAlchemyUnitOfWork = Depends(uow_dep)) -> TransferResult:
    src, dst = transfer_funds(
        uow,
        from_account_id=payload.from_account_id,
        to_account_id=payload.to_account_id,
        amount_cents=payload.amount_cents,
    )
    assert src.id is not None
    assert dst.id is not None
    return TransferResult(
        from_account=AccountRead(id=src.id, owner=src.owner, balance_cents=src.balance_cents),
        to_account=AccountRead(id=dst.id, owner=dst.owner, balance_cents=dst.balance_cents),
    )

