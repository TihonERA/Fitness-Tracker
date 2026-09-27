import pytest

from Backend.tests.unit.trainings.training_day.day_exercises.helpers import (
    create_day_exercises,
    create_tr_day,
    create_tr_day_with_day_exercises,
    get_exercise_order,
)
from Backend.tests.unit.trainings.training_day.helpers import get_exercise_id_order
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    DayExerciseNotFound,
    DayExerciseOrderIntegrityError,
)


def test_success() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    training_day.update_exercise(exercise_id=2, exercise_order=3)

    assert get_exercise_id_order(training_day) == [1, 3, 2]
    assert get_exercise_order(training_day) == [1, 2, 3]


def test_last_to_middle() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.update_exercise(exercise_id=10, exercise_order=5)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4, 10, 5, 6, 7, 8, 9]
    assert get_exercise_order(training_day) == list(range(1, 11))


def test_last_to_beggining() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.update_exercise(exercise_id=10, exercise_order=1)

    assert get_exercise_id_order(training_day) == [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert get_exercise_order(training_day) == list(range(1, 11))


def test_first_to_end() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.update_exercise(exercise_id=1, exercise_order=10)

    assert get_exercise_id_order(training_day) == [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]
    assert get_exercise_order(training_day) == list(range(1, 11))


def test_first_to_middle() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.update_exercise(exercise_id=1, exercise_order=5)

    assert get_exercise_id_order(training_day) == [2, 3, 4, 5, 1, 6, 7, 8, 9, 10]
    assert get_exercise_order(training_day) == list(range(1, 11))


def test_middle_to_beggining() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.update_exercise(exercise_id=5, exercise_order=1)

    assert get_exercise_id_order(training_day) == [5, 1, 2, 3, 4, 6, 7, 8, 9, 10]
    assert get_exercise_order(training_day) == list(range(1, 11))


def test_middle_to_end() -> None:
    training_day = create_tr_day_with_day_exercises(count_of_day_exercises=10)

    assert get_exercise_id_order(training_day) == list(range(1, 11))

    training_day.update_exercise(exercise_id=5, exercise_order=10)

    assert get_exercise_id_order(training_day) == [1, 2, 3, 4, 6, 7, 8, 9, 10, 5]
    assert get_exercise_order(training_day) == list(range(1, 11))


def test_invalid_order_gap() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_order(training_day) == [1, 2, 3]

    with pytest.raises(DayExerciseOrderIntegrityError):
        training_day.update_exercise(exercise_id=1, exercise_order=4)


def test_invalid_order() -> None:
    training_day = create_tr_day()

    with pytest.raises(DayExerciseOrderIntegrityError):
        training_day.update_exercise(exercise_id=1, exercise_order=0)


def test_not_found() -> None:
    training_day = create_tr_day_with_day_exercises()

    assert get_exercise_id_order(training_day) == [1, 2, 3]

    with pytest.raises(DayExerciseNotFound):
        training_day.update_exercise(exercise_id=4, exercise_order=1)
