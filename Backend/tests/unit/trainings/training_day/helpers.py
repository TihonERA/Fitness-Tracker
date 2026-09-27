from Backend.trainings.domain.training_day_model import TrainingDay


def assert_same_tr_days(tr_day1: TrainingDay, tr_day2: TrainingDay) -> None:
    assert tr_day1.id is not None
    assert tr_day2.id is not None

    assert tr_day1.id == tr_day2.id
    assert tr_day1.workout_id == tr_day2.workout_id
    assert tr_day1.name == tr_day2.name
    assert tr_day1.day_order == tr_day2.day_order


def create_day_exercises(training_day: TrainingDay, count: int = 3) -> None:
    for i in range(1, count + 1):
        training_day.add_exercise(exercise_id=i, exercise_order=i)


def get_exercise_id_order(training_day: TrainingDay) -> list[int]:
    return [ex.exercise_id for ex in training_day.day_exercises]
