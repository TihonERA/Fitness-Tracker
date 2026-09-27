from Backend.tests.unit.trainings.training_day.helpers import create_day_exercises
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle

NOT_BINDED_TO_WORKOUT = -1


def create_tr_day() -> TrainingDay:
    return TrainingDay.create(
        workout_id=NOT_BINDED_TO_WORKOUT, name=EntityTitle("day"), day_order=DayOrder(1)
    )


def create_tr_day_with_day_exercises(count_of_day_exercises: int = 3) -> TrainingDay:
    training_day = create_tr_day()

    create_day_exercises(training_day, count_of_day_exercises)

    return training_day


def get_exercise_order(training_day: TrainingDay) -> list[int]:
    return [ex.exercise_order.value for ex in training_day.day_exercises]
