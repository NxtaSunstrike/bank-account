from typing import Self
from dataclasses import dataclass

from app.domain.event_manager import EventManager
from app.domain.value_objects import AccountId, Amount
from app.domain.events import AccountCreated, AccountCredited, AccountDebited, WithdrawalLimitChanged
from app.domain.exceptions import WithdrawError


@dataclass
class Account(EventManager):
    id: AccountId
    balance: Amount
    withdrawal_limit: Amount

    @staticmethod
    def create_account(
        id: AccountId, balance: Amount = 0.0
    ) -> 'Account': 
        account: Account = Account(
            id=id, 
            balance=balance,
            withdrawal_limit=Amount(1000.0)
        )
        event: AccountCreated = AccountCreated(
            account_id=id.id,
            balance=balance.amount
        )
        account.add_event(event=event)
        return Account

    def withdraw(self: Self, amount: Amount) -> None:
        if amount > self.withdrawal_limit.amount:
            raise WithdrawError('Withdrawal limit exceeded')

        if amount > self.balance.amount:
            raise WithdrawError('Insufficient funds')
        
        self.balance.amount -= amount.amount
        event: AccountDebited = AccountDebited(
            account_id=self.id.id,
            amount=amount.amount
        )
        self.add_event(event=event)
    
    def deposit(self: Self, amount: Amount) -> None:
        self.balance.amount += amount.amount
        event: AccountCredited = AccountCredited(
            account_id=self.id.id,
            amount=amount.amount
        )
        self._upgrade_limit(amount=Amount(500.0))
        self.add_event(event=event)

    def _upgrade_limit(self: Self, amount: Amount) -> None:
        self.withdrawal_limit.amount += amount.amount
        event: WithdrawalLimitChanged = WithdrawalLimitChanged(
            account_id=self.id.id,
            withdrawal_limit=self.withdrawal_limit.amount
        )
        self.add_event(event=event)