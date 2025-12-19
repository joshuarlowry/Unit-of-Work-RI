from __future__ import annotations

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    owner: str = Field(min_length=1, max_length=200)
    initial_balance_cents: int = Field(default=0, ge=0)


class AccountRead(BaseModel):
    id: int
    owner: str
    balance_cents: int


class TransferCreate(BaseModel):
    from_account_id: int = Field(ge=1)
    to_account_id: int = Field(ge=1)
    amount_cents: int = Field(ge=1)


class TransferResult(BaseModel):
    from_account: AccountRead
    to_account: AccountRead

