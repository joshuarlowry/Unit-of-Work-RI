from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions import InsufficientFunds, InvalidTransferAmount


@dataclass
class Account:
    id: int | None
    owner: str
    balance_cents: int

    def deposit(self, amount_cents: int) -> None:
        if amount_cents <= 0:
            raise InvalidTransferAmount("deposit amount must be positive")
        self.balance_cents += amount_cents

    def withdraw(self, amount_cents: int) -> None:
        if amount_cents <= 0:
            raise InvalidTransferAmount("withdrawal amount must be positive")
        if self.balance_cents < amount_cents:
            raise InsufficientFunds("insufficient funds")
        self.balance_cents -= amount_cents

