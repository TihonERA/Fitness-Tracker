from uuid import UUID, uuid4
import uuid

import pytest

from faker import Faker

from Backend.trainings.application.dto.workout import (
    CreateWorkoutCommand,
    UpdateWorkoutCommand,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout


class WorkoutDTOFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def make_create_workout_command(
        self,
        name: str | None = None,
        description: str | None = None,
        public: bool = False,
    ) -> CreateWorkoutCommand:
        return CreateWorkoutCommand(
            user_id=uuid4(),
            name=name if name is not None else self.faker.name(),
            description=description,
            public=public,
        )

    def make_update_workout_command(
        self,
        user_id: UUID,
        workout_id: int,
        name: str | None = None,
        description: str | None = None,
        public: bool = False,
    ) -> UpdateWorkoutCommand:
        return UpdateWorkoutCommand(
            user_id=user_id,
            workout_id=workout_id,
            name=name,
            description=description,
            public=public,
        )
