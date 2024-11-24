from typing import Self
from uuid import UUID
from decimal import Decimal

from app.domain.value_objects import AccountId, Amount
from app.domain.bank_account import BankAccount
from app.application.interfaces import EventStoreInterface, EventBusInterface
from app.domain.events import BaseDomainEvent
from app.domain.factories import BankAccountFactory


class CreateAccountCommandHandler:
    def __init__(
            self: Self, 
            event_store: EventStoreInterface, 
            event_bus: EventBusInterface,
        ) -> None:
        self.event_store: EventStoreInterface = event_store
        self.event_bus: EventBusInterface = event_bus

    async def __call__(self: Self, account_id: UUID, balance: Decimal) -> None:
        bank_account: BankAccount = BankAccountFactory.create_account(
            id=AccountId(account_id),
            balance=Amount(balance)
        )
        events: list[BaseDomainEvent] = bank_account.push_events()

        await self.event_store.add_to_storage(events=events)
        await self.event_bus.publish_to_queue(events=events)


class DebitAcountCommandHandler:
    def __init__(
            self: Self,
            event_store: EventStoreInterface,
            event_bus: EventBusInterface,
        ) -> None:
        self.event_store: EventStoreInterface = event_store
        self.event_bus: EventBusInterface = event_bus

    async def __call__(self: Self, account_id: UUID, amount: Decimal) -> None:
        fetched_events: list[BaseDomainEvent] = await self.event_store.get_events(aggregate_id=account_id)
        account: BankAccount = await BankAccountFactory.get_bank_account_state(fetched_events)
        account.deposit(amount=Amount(amount))
        events: list[BaseDomainEvent] = account.push_events()

        await self.event_store.add_to_storage(events=events)
        await self.event_bus.publish_to_queue(events=events)


class CreditAccountCommandHandler:
    def __init__(
            self: Self,
            event_store: EventStoreInterface,
            event_bus: EventBusInterface,
        ) -> None:
        self.event_store: EventStoreInterface = event_store
        self.event_bus: EventBusInterface = event_bus

    async def __call__(self: Self, account_id: UUID, amount: Decimal) -> None:
        fetched_events: list[BaseDomainEvent] = await self.event_store.get_events(aggregate_id=account_id)
        account: BankAccount = await BankAccountFactory.get_bank_account_state(fetched_events)
        account.withdraw(amount=Amount(amount))
        events: list[BaseDomainEvent] = account.push_events()

        await self.event_store.add_to_storage(events=events)
        await self.event_bus.publish_to_queue(events=events)
