from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class BaseDomainEvent:
    agregate_id: UUID
    event_timestamp: datetime = field(default_factory=datetime.now, init=False)


@dataclass(frozen=True)
class AccountCreated(BaseDomainEvent):
    account_id: UUID
    balance: Decimal
    withdrawal_limit: Decimal


@dataclass(frozen=True)
class AccountCredited(BaseDomainEvent):
    account_id: UUID
    amount: Decimal


@dataclass(frozen=True)
class AccountDebited(BaseDomainEvent):
    account_id: UUID
    amount: Decimal


@dataclass(frozen=True)
class WithdrawalLimitChanged(BaseDomainEvent):
    account_id: UUID
    amount: Decimal

