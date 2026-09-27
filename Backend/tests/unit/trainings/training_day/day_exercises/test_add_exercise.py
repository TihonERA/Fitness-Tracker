import pytest

from Backend.tests.unit.trainings.training_day.day_exercises.helpers import (
    create_tr_day,
    create_tr_day_with_day_exercises,
    get_exercise_id_order,
    get_exercise_order,
)
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseOrderIntegrityError,
)
from Backend.trainings.domain.training_day_model import TrainingDay


def test_add_exercise_success() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.add_exercise(exercise_id=4, exercise_order=4)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4]
    assert get_exercise_order(training_day) == [1, 2, 3, 4]


def test_add_exercise_at_beginning() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.add_exercise(exercise_id=4, exercise_order=1)

    assert get_exercise_id_order(training_day) == [4, 1, 2, 3]
    assert get_exercise_order(training_day) == [1, 2, 3, 4]


def test_add_exercise_at_middle() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=5)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4, 5]

    training_day.add_exercise(exercise_id=6, exercise_order=3)

    assert get_exercise_id_order(training_day) == [1, 2, 6, 3, 4, 5]
    assert get_exercise_order(training_day) == [1, 2, 3, 4, 5, 6]


def test_add_exercise_at_end() -> None:
    training_day = create_tr_day_with_day_exercises()

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
