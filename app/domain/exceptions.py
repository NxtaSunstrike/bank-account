from typing import Self


class DomainError(Exception):
    def __init__(self: Self, messgae: str) -> None:
        super.__init__(messgae)

class ValidationError(DomainError):
    ...

class WithdrawError(DomainError):
    ...

class StateRestoringError(DomainError):
    ...