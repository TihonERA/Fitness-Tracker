from Backend.trainings.domain.training_day_model import TrainingDay
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


def create_tr_day_with_day_exercises(count_of_day_exercises: int = 3) -> TrainingDay:
    training_day = create_tr_day()

    create_day_exercises(training_day, count_of_day_exercises)

    return training_day


def get_exercise_id_order(training_day: TrainingDay) -> list[int]:
    return [ex.exercise_id for ex in training_day.day_exercises]


def get_exercise_order(training_day: TrainingDay) -> list[int]:
    return [ex.exercise_order.value for ex in training_day.day_exercises]
