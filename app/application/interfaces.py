from typing import Self, Protocol
from abc import abstractmethod

from app.domain.events import BaseDomainEvent
from app.domain.value_objects import AccountId


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