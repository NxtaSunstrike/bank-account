from typing import Self, Protocol
from abc import abstractmethod


class UnitOfWorkInterface(Protocol):
    @abstractmethod
    async def commit(self: Self) -> None:
        raise NotImplementedError("commit() must be implemented")

    @abstractmethod
    async def rollback(self: Self) -> None:
        raise NotImplementedError("rollback() must be implemented")