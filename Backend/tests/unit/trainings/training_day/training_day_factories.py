from random import randint
from uuid import UUID

from faker import Faker

from Backend.trainings.application.dto.training_day import (
    CreateDayExerciseCommand,
    CreateTrainingDayCommand,
)


class TrainingDayDTOFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def make_create_tr_day_command(
        self,
        user_id: UUID,
        workout_id: int,
        name: str | None = None,
        day_order: int | None = None,
    ) -> CreateTrainingDayCommand:
        return CreateTrainingDayCommand(
            user_id=user_id,
            workout_id=workout_id,
            name=name if name is not None else self.faker.name(),
            day_order=day_order if day_order is not None else randint(1, 7),
        )


class DayExerciseDTOFactory:
    def __init__(self, faker: Faker) -> None:
        self.faker = faker

    def make_create_day_exercise_command(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int | None = None,
        exercise_order: int | None = None,
    ) -> CreateDayExerciseCommand:
        return CreateDayExerciseCommand(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id,
            exercise_id=exercise_id or randint(1, 10),
            exercise_order=exercise_order or 1,
        )
