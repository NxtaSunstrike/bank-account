from typing import Self, Protocol
from abc import abstractmethod

from app.domain.events import BaseDomainEvent


class IventBusInterface(Protocol):
    @abstractmethod
    async def publish_to_queue(self: Self, events: list[BaseDomainEvent]) -> None:
        raise NotImplementedError('method must be implemented by subclasses')