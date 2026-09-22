from uuid import uuid4

import pytest

from faker import Faker

from Backend.trainings.application.dto.workout import CreateWorkoutCommand
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout


class WorkoutDTOFactory:
    @staticmethod
    def make_create_workout_command(
        name: str | None = None,
        description: str | None = None,
        public: bool = False,
    ) -> CreateWorkoutCommand:
        return CreateWorkoutCommand(
            user_id=uuid4(),
            name=EntityTitle(name if name is not None else Faker().name()),
            description=description,
            public=public,
        )
