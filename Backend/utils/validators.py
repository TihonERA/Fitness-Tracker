from typing import TypeGuard
from uuid import UUID

from Backend.models.base import Base
from Backend.models.workout import Workout


def check_instance_ownership[ModelT: Base](
    instance: ModelT, user_id: UUID
) -> TypeGuard[ModelT]:
    return getattr(instance, "user_id", None) == user_id
