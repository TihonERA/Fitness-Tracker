from dataclasses import dataclass

from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseOrderIntegrityError,
)


@dataclass(frozen=True)
class ExerciseOrder:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise DayExerciseOrderIntegrityError("Exercise order must be at least 1")
