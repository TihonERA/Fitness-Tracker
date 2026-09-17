from uuid import UUID
from Backend.trainings.api.schemas.workout import WorkoutCreate


class WorkoutCreateDTO(WorkoutCreate):
    user_id: UUID
