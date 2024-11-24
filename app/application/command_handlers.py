from typing import Self
from uuid import UUID
from decimal import Decimal

from app.domain.value_objects import AccountId, Amount
from app.domain.bank_account import BankAccount
from app.application.interfaces import EventStoreInterface, EventBusInterface, UnitOfWorkInterface
from app.domain.events import BaseDomainEvent


class CreateAccountCommandHandler:
    def __init__(
            self: Self, 
            event_store: EventStoreInterface, 
            event_bus: EventBusInterface,
            uow: UnitOfWorkInterface
        ) -> None:
        self.event_store: EventStoreInterface = event_store
        self.event_bus: EventBusInterface = event_bus
        self.uow: UnitOfWorkInterface = uow
    
    async def __call__(self: Self, account_id: UUID, balance: Decimal) -> None:
        bank_account: BankAccount = BankAccount.create_account(
            id=AccountId(account_id),
            balance=Amount(balance)
        )
        events: list[BaseDomainEvent] = bank_account.push_events()

        await self.event_store.add_to_storage(events=events)
        await self.event_bus.publish_to_queue(events=events)
        await self.uow.commit()


class DebitAcountCommandHandler:
    def __init__(
            self: Self,
            event_store: EventStoreInterface,
            event_bus: EventBusInterface,
            uow: UnitOfWorkInterface
        ) -> None:
        self.event_store: EventStoreInterface = event_store
        self.event_bus: EventBusInterface = event_bus
        self.uow: UnitOfWorkInterface = uow

    async def __call__(self: Self, account_id: UUID, amount: Decimal) -> None:
        account: BankAccount = ...
        account.deposit(amount=Amount(amount))
        events: list[BaseDomainEvent] = account.push_events()

        await self.event_store.add_to_storage(events=events)
        await self.event_bus.publish_to_queue(events=events)
        await self.uow.commit()


class CreditAccountCommandHandler:
    def __init__(
            self: Self,
            event_store: EventStoreInterface,
            event_bus: EventBusInterface,
            uow: UnitOfWorkInterface
        ) -> None:
        self.event_store: EventStoreInterface = event_store
        self.event_bus: EventBusInterface = event_bus
        self.uow: UnitOfWorkInterface = uow

    async def __call__(self: Self, account_id: UUID, amount: Decimal) -> None:
        account: BankAccount = ...
        account.withdraw(amount=Amount(amount))
        events: list[BaseDomainEvent] = account.push_events()

        await self.event_store.add_to_storage(events=events)
        await self.event_bus.publish_to_queue(events=events)
        await self.uow.commit()
