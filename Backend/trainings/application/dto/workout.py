from dataclasses import dataclass
from uuid import UUID

from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass
class CreateWorkoutCommand:
    user_id: UUID
    name: EntityTitle
    description: str | None = None
    public: bool = False


@dataclass
class UpdateWorkoutCommand:
    user_id: UUID
    workout_id: int
    name: EntityTitle | None = None
    description: str | None = None
    public: bool | None = None
