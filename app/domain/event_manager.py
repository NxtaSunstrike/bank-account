from typing import Self
from dataclasses import dataclass, field

from app.domain.events import BaseDomainEvent


@dataclass
class EventManager:
    _events: list[BaseDomainEvent] = field(default_factory=list, init=False)

    def add_event(self: Self, event: BaseDomainEvent) -> None:
        self._events.append(event)

    def push_events(self: Self) -> list[BaseDomainEvent]:
        events: list[BaseDomainEvent] = self._events.copy()
        self._events.clear()
        return events
