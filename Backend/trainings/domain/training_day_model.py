from dataclasses import dataclass

from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseNotFound,
    DayExerciseOrderIntegrityError,
)
from Backend.trainings.domain.value_objects import exercise_order
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.exercise_order import ExerciseOrder
from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass
class TrainingDay:
    id: int | None
    workout_id: int
    name: EntityTitle
    day_order: DayOrder
    day_exercises: list[DayExercise]

    @classmethod
    def create(
        cls, workout_id: int, name: EntityTitle, day_order: DayOrder
    ) -> "TrainingDay":
        return cls(
            id=None,
            workout_id=workout_id,
            name=name,
            day_order=day_order,
            day_exercises=[],
        )

    def update(
        self, name: EntityTitle | None = None, day_order: DayOrder | None = None
    ) -> None:
        if name:
            self.name = name

        if day_order:
            self.day_order = day_order

    def _sort_day_exercises_by_order(self) -> None:
        self.day_exercises.sort(key=lambda x: x.exercise_order.value)

    def _validate_exercise_order_in_sorted_day_exercises(
        self, exercise_order: int
    ) -> None:
        if self.day_exercises == []:
            return

        if exercise_order - 1 > self.day_exercises[-1].exercise_order.value:
            raise DayExerciseOrderIntegrityError(
                f"New exercise order must be between existing exercises, got {exercise_order}"
            )

    def _reindex(self) -> None:
        for order, day in enumerate(self.day_exercises, start=1):
            day.exercise_order = ExerciseOrder(order)

    def add_exercise(self, exercise_id: int, exercise_order: int) -> None:
        self._sort_day_exercises_by_order()
        self._validate_exercise_order_in_sorted_day_exercises(exercise_order)

        exercise = DayExercise(
            day_id=self.id,
            exercise_id=exercise_id,
            exercise_order=ExerciseOrder(exercise_order),
        )

        self.day_exercises.insert(exercise_order - 1, exercise)

        self._reindex()

    def _find_exercise(self, exercise_id: int) -> DayExercise:
        exercise = next(
            (e for e in self.day_exercises if e.exercise_id == exercise_id), None
        )

        if exercise is None:
            raise DayExerciseNotFound(exercise_id)

        return exercise

    def update_exercise(self, exercise_id: int, exercise_order: int) -> None:
        self._sort_day_exercises_by_order()
        self._validate_exercise_order_in_sorted_day_exercises(exercise_order)

        exercise = self._find_exercise(exercise_id)
        exercise.exercise_order = ExerciseOrder(exercise_order)

        self.day_exercises.remove(exercise)
        self.day_exercises.insert(exercise_order - 1, exercise)

        self._reindex()

    def delete_exercise(self, exercise_id: int) -> None:
        self._sort_day_exercises_by_order()
        exercise = self._find_exercise(exercise_id)

        self.day_exercises.remove(exercise)

        self._reindex()
