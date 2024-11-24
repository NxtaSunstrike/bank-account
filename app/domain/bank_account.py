from typing import Self
from dataclasses import dataclass

from app.domain.event_manager import EventManager
from app.domain.value_objects import AccountId, Amount
from app.domain.events import AccountCredited, AccountDebited, WithdrawalLimitChanged, BaseDomainEvent
from app.domain.exceptions import WithdrawError


@dataclass
class BankAccount(EventManager):
    id: AccountId
    balance: Amount
    withdrawal_limit: Amount

    def withdraw(self: Self, amount: Amount) -> None:
        if event.amount > self.withdrawal_limit.amount:
            raise WithdrawError('Withdrawal limit exceeded')
        if event.amount > self.balance.amount:
            raise WithdrawError('Insufficient funds')
        event: AccountDebited = AccountDebited(
            agregate_id=self.id.uuid,
            account_id=self.id.uuid,
            amount=amount.amount
        )
        self._apply(event=event)
        self.add_event(event=event)
    
    def deposit(self: Self, amount: Amount) -> None:
        event: AccountCredited = AccountCredited(
            agregate_id=self.id.uuid,
            account_id=self.id.uuid,
            amount=amount.amount
        )
        self._apply(event=event)
        self.add_event(event=event)
        self._upgrade_limit(amount=Amount(500.0))

    def _upgrade_limit(self: Self, amount: Amount) -> None:
        event: WithdrawalLimitChanged = WithdrawalLimitChanged(
            agregate_id=self.id.uuid,
            account_id=self.id.uuid,
            withdrawal_limit=self.withdrawal_limit.amount
        )
        self._apply(event=event)
        self.add_event(event=event)

    def _apply(self: Self, event: BaseDomainEvent) -> None:
        if isinstance(event, AccountCredited):
            self.balance.amount += event.amount
        if isinstance(event, AccountDebited):
            self.balance.amount -= event.amount
        if isinstance(event, WithdrawalLimitChanged):
            self.withdrawal_limit.amount += event.amount