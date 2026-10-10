from dataclasses import dataclass
from uuid import UUID

from Backend.trainings.application.dto.training_day import TrainingDayReadDTO
from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass
class CreateWorkoutCommand:
    user_id: UUID
    name: str
    description: str | None = None
    public: bool = False


@dataclass
class UpdateWorkoutCommand:
    user_id: UUID
    workout_id: int
    name: str | None = None
    description: str | None = None
    public: bool | None = None


@dataclass(frozen=True)
class WorkoutReadDTO:
    id: int
    user_id: UUID
    name: str
    description: str | None
    public: bool


@dataclass(frozen=True)
class WorkoutDetailDTO(WorkoutReadDTO):
    training_days: list[TrainingDayReadDTO]
