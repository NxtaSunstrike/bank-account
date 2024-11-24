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
        id: AccountId, balance: Amount
    ) -> 'Account': 
        withdrawal_limit=Amount(1000.0)
        account: Account = Account(
            id=id.uuid, 
            balance=balance.amount,
            withdrawal_limit=withdrawal_limit.amount
        )
        event: AccountCreated = AccountCreated(
            agregate_id=id.uuid,
            account_id=id.uuid,
            balance=balance.amount,
            withdrawal_limit=withdrawal_limit.amount
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
            agregate_id=self.id.uuid,
            account_id=self.id.uuid,
            amount=amount.amount
        )
        self.add_event(event=event)
    
    def deposit(self: Self, amount: Amount) -> None:
        self.balance.amount += amount.amount
        event: AccountCredited = AccountCredited(
            agregate_id=self.id.uuid,
            account_id=self.id.uuid,
            amount=amount.amount
        )
        self.add_event(event=event)
        self._upgrade_limit(amount=Amount(500.0))

    def _upgrade_limit(self: Self, amount: Amount) -> None:
        self.withdrawal_limit.amount += amount.amount
        event: WithdrawalLimitChanged = WithdrawalLimitChanged(
            agregate_id=self.id.uuid,
            account_id=self.id.uuid,
            withdrawal_limit=self.withdrawal_limit.amount
        )
        self.add_event(event=event)