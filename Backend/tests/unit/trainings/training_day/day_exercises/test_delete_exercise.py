import pytest

from Backend.tests.unit.trainings.training_day.day_exercises.helpers import (
    create_tr_day_with_day_exercises,
    get_exercise_order,
)
from Backend.tests.unit.trainings.training_day.helpers import get_exercise_id_order
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseNotFound,
)


def test_success() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.delete_exercise(exercise_id=3)

    assert get_exercise_id_order(training_day) == [1, 2]
    assert get_exercise_order(training_day) == [1, 2]


def test_delete_in_beggining() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.delete_exercise(exercise_id=1)

    assert get_exercise_id_order(training_day) == list(range(2, 11))
    assert get_exercise_order(training_day) == list(range(1, 10))


def test_delete_in_middle() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.delete_exercise(exercise_id=5)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4, 6, 7, 8, 9, 10]
    assert get_exercise_order(training_day) == list(range(1, 10))


def test_not_found() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    with pytest.raises(DayExerciseNotFound):
        training_day.delete_exercise(exercise_id=4)
