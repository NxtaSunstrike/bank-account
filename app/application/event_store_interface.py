from typing import Self, Protocol
from abc import abstractmethod

from app.domain.events import BaseDomainEvent
from app.domain.value_objects import AccountId


class EventStoreInterface(Protocol):
    @abstractmethod
    async def add_to_storage(self: Self, events: list[BaseDomainEvent]) -> None:
        raise NotImplementedError('method must be implemented by subclasses')
    
    @abstractmethod
    async def get_events(self: Self, aggregate_id: AccountId) -> list[BaseDomainEvent]:
        raise NotImplementedError('method must be implemented by subclasses')