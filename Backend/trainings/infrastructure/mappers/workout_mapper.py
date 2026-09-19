from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
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
