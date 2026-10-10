from Backend.trainings.application.dto.training_day import (
    DayExerciseReadDTO,
    TrainingDayDetailDTO,
)
from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.exercise_order import ExerciseOrder
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel


class TrainingDayMapper:
    @staticmethod
    def to_orm(training_day: TrainingDay) -> TrainingDayModel:
        return TrainingDayModel(
            workout_id=training_day.workout_id,
            name=training_day.name.value,
            day_order=training_day.day_order.value,
        )

    @staticmethod
    def to_orm_day_exercise(day_exercise: DayExercise) -> DayExerciseModel:
        return DayExerciseModel(
            day_id=day_exercise.day_id,
            exercise_id=day_exercise.exercise_id,
            exercise_order=day_exercise.exercise_order.value,
        )

    @staticmethod
    def to_domain_day_exercises(
        day_exercises: list[DayExerciseModel],
    ) -> list[DayExercise]:
        return [
            DayExercise(
                day_id=d.day_id,
                exercise_id=d.exercise_id,
                exercise_order=ExerciseOrder(d.exercise_order),
            )
            for d in day_exercises
        ]

    @classmethod
    def to_domain(cls, training_day_model: TrainingDayModel) -> TrainingDay:
        return TrainingDay(
            id=training_day_model.id,
            workout_id=training_day_model.workout_id,
            name=EntityTitle(training_day_model.name),
            day_order=DayOrder(training_day_model.day_order),
            day_exercises=cls.to_domain_day_exercises(training_day_model.day_exercises),
        )

    @staticmethod
    def _to_dto_day_exercise(day_exercise: DayExerciseModel) -> DayExerciseReadDTO:
        return DayExerciseReadDTO(
            day_id=day_exercise.day_id,
            exercise_id=day_exercise.exercise_id,
            exercise_order=day_exercise.exercise_order,
        )

    @classmethod
    def to_dto(cls, training_day: TrainingDayModel) -> TrainingDayDetailDTO:
        return TrainingDayDetailDTO(
            id=training_day.id,
            workout_id=training_day.workout_id,
            name=training_day.name,
            day_order=training_day.day_order,
            day_exercises=[
                cls._to_dto_day_exercise(d) for d in training_day.day_exercises
            ],
        )
