from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel
from Backend.trainings.infrastructure.models.workout import WorkoutModel


class WorkoutMapper:
    def _make_day_exercise(self, exercise_model: DayExerciseModel) -> DayExercise:
        return DayExercise(
            day_id=exercise_model.day_id,
            exercise_id=exercise_model.exercise_id,
            day_order=exercise_model.day_order,
        )

    def _make_training_day(self, day_model: TrainingDayModel) -> TrainingDay:
        return TrainingDay(
            id=day_model.id,
            workout_id=day_model.workout_id,
            name=day_model.name,
            day_exercises=[self._make_day_exercise(e) for e in day_model.day_exercises],
        )

    @staticmethod
    def _to_domain_base(workout_model: WorkoutModel) -> Workout:
        return Workout(
            id=workout_model.id,
            user_id=workout_model.user_id,
            name=workout_model.name,
            description=workout_model.description,
            public=workout_model.public,
            training_days=[],
        )

    def to_domain(self, workout_model: WorkoutModel) -> Workout:
        return self._to_domain_base(workout_model)

    def to_domain_with_training_days(self, workout_model: WorkoutModel) -> Workout:
        workout = self._to_domain_base(workout_model)

        workout.training_days = [
            self._make_training_day(d) for d in workout_model.training_days
        ]

        return workout

    def to_domain_with_inherited_training_days(
        self, workout_model: WorkoutModel, inherited_training_days: list[TrainingDay]
    ) -> Workout:
        workout = self._to_domain_base(workout_model)

        workout.training_days = inherited_training_days

        return workout

    def to_orm(self, workout: Workout) -> WorkoutModel:
        return WorkoutModel(
            user_id=workout.user_id,
            name=workout.name,
            description=workout.description,
            public=workout.public,
        )
