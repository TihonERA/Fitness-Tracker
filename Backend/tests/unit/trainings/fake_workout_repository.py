from Backend.trainings.domain.workout_model import Workout
from copy import copy


class FakeWorkoutRepository:
    def __init__(self) -> None:
        self.fake_db: dict[int, Workout] = {}

    def _get_from_db(self, id: int) -> Workout | None:
        return self.fake_db.get(id, None)

    async def get_loaded(self, id: int) -> Workout | None:
        return copy(self._get_from_db(id))

    async def get(self, id: int) -> Workout | None:
        return copy(self._get_from_db(id))

    async def create(self, workout: Workout) -> Workout:
        if len(self.fake_db) == 0:
            workout.id = 1
            self.fake_db[workout.id] = copy(workout)

            return copy(workout)

        last_id = list(self.fake_db.keys())[-1]
        workout.id = last_id + 1

        self.fake_db[workout.id] = copy(workout)
        return copy(workout)

    async def save(self, workout: Workout) -> Workout | None:
        if workout.id is None:
            return None

        workout_db = self._get_from_db(workout.id)

        if workout_db is None:
            return None

        workout_db.name = workout.name
        workout_db.description = workout.description
        workout_db.public = workout.public

        return copy(workout_db)

    async def delete(self, workout: Workout) -> None:
        if workout.id is None:
            return
        self.fake_db.pop(workout.id)
