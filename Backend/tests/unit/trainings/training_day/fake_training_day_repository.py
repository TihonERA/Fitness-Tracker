from Backend.trainings.application.exceptions.training_day import (
    TrainingDayConcurrencyError,
    TrainingDayNotCreatedError,
)
from Backend.trainings.domain.training_day_model import TrainingDay

from copy import deepcopy


class FakeTrainingDayRepository:
    def __init__(self) -> None:
        self.fake_db: dict[int, TrainingDay] = {}

    def _get_from_db(self, id: int) -> TrainingDay | None:
        return self.fake_db.get(id, None)

    async def get(self, id: int) -> TrainingDay | None:
        return deepcopy(self._get_from_db(id))

    async def create(self, training_day: TrainingDay) -> TrainingDay:
        if len(self.fake_db) == 0:
            training_day.id = 1

            self.fake_db[training_day.id] = deepcopy(training_day)
            return deepcopy(training_day)

        last_id = list(self.fake_db.keys())[-1]
        training_day.id = last_id + 1

        self.fake_db[training_day.id] = deepcopy(training_day)
        return deepcopy(training_day)

    async def save(self, training_day: TrainingDay) -> TrainingDay:
        if training_day.id is None:
            raise TrainingDayNotCreatedError()

        training_day_db = self._get_from_db(training_day.id)

        if training_day_db is None:
            raise TrainingDayConcurrencyError(training_day.id)

        training_day_db = deepcopy(training_day)

        return deepcopy(training_day)

    async def delete(self, id: int) -> None:
        self.fake_db.pop(id)
