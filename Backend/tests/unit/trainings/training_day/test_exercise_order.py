import pytest

from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseOrderIntegrityError,
)
from Backend.trainings.domain.value_objects.exercise_order import ExerciseOrder


def test_under_lowest_border() -> None:
    with pytest.raises((DayExerciseOrderIntegrityError)):
        ExerciseOrder(0)
