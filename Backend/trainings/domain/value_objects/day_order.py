from dataclasses import dataclass

from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayOrderError,
)


@dataclass(frozen=True)
class DayOrder:
    value: int

    def __post_init__(self) -> None:
        if not (1 <= self.value <= 7):
            raise TrainingDayOrderError(self.value)
