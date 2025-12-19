class DomainError(Exception):
    """Base domain exception."""


class InsufficientFunds(DomainError):
    pass


class InvalidTransferAmount(DomainError):
    pass


class AccountNotFound(DomainError):
    pass

