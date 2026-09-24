from random import randint
from uuid import UUID

from faker import Faker

from Backend.trainings.application.dto.training_day import CreateTrainingDayCommand
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle


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
