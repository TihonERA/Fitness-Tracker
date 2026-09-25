from _pytest.fixtures import traverse_fixture_closure
import pytest

from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseOrderIntegrityError,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects import exercise_order
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle

NOT_BINDED_TO_WORKOUT = -1


def create_tr_day() -> TrainingDay:
    return TrainingDay.create(
        workout_id=NOT_BINDED_TO_WORKOUT, name=EntityTitle("day"), day_order=DayOrder(1)
    )


def create_day_exercises(training_day: TrainingDay, count: int = 3) -> None:
    for i in range(1, count + 1):
        training_day.add_exercise(exercise_id=i, exercise_order=i)


def get_exercise_id_order(training_day: TrainingDay) -> list[int]:
    return [ex.exercise_id for ex in training_day.day_exercises]


def get_exercise_order(training_day: TrainingDay) -> list[int]:
    return [ex.exercise_order.value for ex in training_day.day_exercises]


def test_add_exercise_success() -> None:
    training_day = create_tr_day()

    create_day_exercises(training_day)

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.add_exercise(exercise_id=4, exercise_order=4)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4]
    assert get_exercise_order(training_day) == [1, 2, 3, 4]


def test_add_exercise_at_beginning() -> None:
    training_day = create_tr_day()

    create_day_exercises(training_day)

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.add_exercise(exercise_id=4, exercise_order=1)

    assert get_exercise_id_order(training_day) == [4, 1, 2, 3]
    assert get_exercise_order(training_day) == [1, 2, 3, 4]


def test_add_exercise_at_middle() -> None:
    training_day = create_tr_day()

    create_day_exercises(training_day, count=5)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4, 5]

    training_day.add_exercise(exercise_id=6, exercise_order=3)

    assert get_exercise_id_order(training_day) == [1, 2, 6, 3, 4, 5]
    assert get_exercise_order(training_day) == [1, 2, 3, 4, 5, 6]


def test_add_exercise_at_end() -> None:
    training_day = create_tr_day()

    create_day_exercises(training_day, count=3)

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.add_exercise(exercise_id=4, exercise_order=4)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4]
    assert get_exercise_order(training_day) == [1, 2, 3, 4]


def test_add_exercise_with_invalid_order_gap() -> None:
    training_day = create_tr_day()

    with pytest.raises(DayExerciseOrderIntegrityError):
        training_day.add_exercise(exercise_id=1, exercise_order=2)


def test_add_exercise_with_invalid_order() -> None:
    training_day = create_tr_day()

    with pytest.raises(DayExerciseOrderIntegrityError):
        training_day.add_exercise(exercise_id=1, exercise_order=0)
