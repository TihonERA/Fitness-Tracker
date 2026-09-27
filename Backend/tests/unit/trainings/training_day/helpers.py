from Backend.trainings.domain.training_day_model import TrainingDay


def assert_same_tr_days(tr_day1: TrainingDay, tr_day2: TrainingDay) -> None:
    assert tr_day1.id is not None
    assert tr_day2.id is not None

    assert tr_day1.id == tr_day2.id
    assert tr_day1.workout_id == tr_day2.workout_id
    assert tr_day1.name == tr_day2.name
    assert tr_day1.day_order == tr_day2.day_order
