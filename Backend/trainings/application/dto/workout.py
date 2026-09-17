from dataclasses import dataclass
from uuid import UUID


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
