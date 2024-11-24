from typing import Self, Protocol
from abc import abstractmethod
from decimal import Decimal

from app.domain.events import BaseDomainEvent
from app.domain.value_objects import AccountId
from app.domain.bank_account import BankAccount
from app.domain.value_objects import Amount


class IventBusInterface(Protocol):
    @abstractmethod
    async def publish_to_queue(self: Self, events: list[BaseDomainEvent]) -> None:
        raise NotImplementedError('method must be implemented by subclasses')
    

class EventStoreInterface(Protocol):
    @abstractmethod
    async def add_to_storage(self: Self, events: list[BaseDomainEvent]) -> None:
        raise NotImplementedError('method must be implemented by subclasses')
    
    @abstractmethod
    async def get_events(self: Self, aggregate_id: AccountId) -> list[BaseDomainEvent]:
        raise NotImplementedError('method must be implemented by subclasses')
    

class UnitOfWorkInterface(Protocol):
    @abstractmethod
    async def commit(self: Self) -> None:
        raise NotImplementedError("commit() must be implemented")

    @abstractmethod
    async def rollback(self: Self) -> None:
        raise NotImplementedError("rollback() must be implemented")


class AccountReader(Protocol):
    @abstractmethod
    async def get_account_balance(self: Self, account_id: AccountId) -> Amount:
        raise NotImplementedError("get_account_balance() must be implemented")
    
    @abstractmethod
    async def get_account(self: Self, account_id: AccountId) -> BankAccount:
        raise NotImplementedError("get_account() must be implemented")


class AccountWriter(Protocol):
    @abstractmethod
    async def create_account(self: Self, account_id: AccountId, balance: Amount) -> None:
        raise NotImplementedError("save_account() must be implemented")
    
    @abstractmethod
    async def credit_account(self: Self, account_id: AccountId, amount: Amount) -> None:
        raise NotImplementedError("credit_account() must be implemented")
    
    @abstractmethod
    async def debit_account(self: Self, account_id: AccountId, amount: Amount) -> None:
        raise NotImplementedError("debit_account() must be implemented")