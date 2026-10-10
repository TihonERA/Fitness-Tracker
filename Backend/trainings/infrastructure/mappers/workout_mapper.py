from Backend.trainings.application.dto.training_day import TrainingDayReadDTO
from Backend.trainings.application.dto.workout import WorkoutDetailDTO, WorkoutReadDTO
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel
from Backend.trainings.infrastructure.models.workout import WorkoutModel


class WorkoutMapper:
    @staticmethod
    def to_domain(workout_model: WorkoutModel) -> Workout:
        return Workout(
            id=workout_model.id,
            user_id=workout_model.user_id,
            name=EntityTitle(workout_model.name),
            description=workout_model.description,
            public=workout_model.public,
        )

    @staticmethod
    def to_orm(workout: Workout) -> WorkoutModel:
        return WorkoutModel(
            user_id=workout.user_id,
            name=workout.name.value,
            description=workout.description,
            public=workout.public,
        )

    @staticmethod
    def _to_dto_tr_day(training_day: TrainingDayModel) -> TrainingDayReadDTO:
        return TrainingDayReadDTO(
            id=training_day.id,
            workout_id=training_day.workout_id,
            name=training_day.name,
            day_order=training_day.day_order,
        )

    @classmethod
    def to_dto_loaded(cls, workout: WorkoutModel) -> WorkoutDetailDTO:
        return WorkoutDetailDTO(
            id=workout.id,
            user_id=workout.user_id,
            name=workout.name,
            description=workout.description,
            public=workout.public,
            training_days=[cls._to_dto_tr_day(t) for t in workout.training_days],
        )

    @staticmethod
    def to_dto_unloaded(workout: WorkoutModel) -> WorkoutReadDTO:
        return WorkoutReadDTO(
            id=workout.id,
            user_id=workout.user_id,
            name=workout.name,
            description=workout.description,
            public=workout.public,
        )
