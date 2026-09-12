from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel

from Backend.models.base import Base, ModelT
from Backend.models.user import User
from Backend.utils.exceptions import Forbidden, NotFound

from Backend.core.interfaces.uow import BaseUOWInterface

from typing import Any, Awaitable, Callable, Coroutine, Sequence, TypeGuard, TypeVar


class BaseService[ModelT: Base, RepoT]:
    @property
    @abstractmethod
    def repository(self) -> RepoT:
        pass
