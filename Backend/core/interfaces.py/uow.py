from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from Backend.utils.uow import UnitOfWork


class BaseUOWInterface(ABC):
    @abstractmethod
    def __aenter__(self) -> "UnitOfWork":
        pass

    @abstractmethod
    def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
