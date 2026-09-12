from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import ColumnElement
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.interfaces import ORMOption

from Backend.models.base import Base


class BaseCreateRepositoryInterface[ModelT: Base](ABC):
    @abstractmethod
    async def create(self, data: BaseModel) -> ModelT:
        pass


class BaseReadRepositoryInterface[ModelT: Base](ABC):
    @abstractmethod
    async def _get_instance_by_column(
        self,
        column: InstrumentedAttribute | ColumnElement,
        search_value: int | UUID | str,
        options: Sequence[ORMOption] | None = None,
    ) -> ModelT | None:
        pass

    @abstractmethod
    async def get(self, id: int | UUID) -> ModelT | None:
        pass


class BaseReadRelationRepositoryInterface[ModelT: Base](ABC):
    @abstractmethod
    async def get_loaded(self, id: int) -> ModelT | None:
        pass


class BaseReadAllRepositoryInterface[ModelT: Base, FilterDTOT: BaseModel](ABC):
    @abstractmethod
    async def get_all(self, data: FilterDTOT) -> Sequence[ModelT]:
        pass


class BaseLockRepositoryInterface[ModelT: Base](ABC):
    @abstractmethod
    async def get_for_update(self, id: int | UUID) -> ModelT | None:
        pass


class BaseUpdateRepositoryInterface[ModelT: Base](ABC):
    @abstractmethod
    async def get_for_update(self, id: int | UUID) -> ModelT | None:
        pass

    @abstractmethod
    async def update(self, instance: ModelT, data: BaseModel) -> ModelT:
        pass


class BaseDeleteRepositoryInterface[ModelT: Base](ABC):
    @abstractmethod
    async def delete(self, id: int | UUID) -> int:
        pass
