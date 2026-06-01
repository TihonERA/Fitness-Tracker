from ..repositories.WorkoutRepository import WorkoutRepository
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.workout import WorkoutScheme, TrainingDayScheme, DayExercisesScheme
from ..models.workout import Workout
from ..models.trainingday import TrainingDay
from ..models.dayexercise import DayExercise


class WorkoutService:

    def __init__(self, db: AsyncSession):
        self.workoutrepo = WorkoutRepository(db=db)
        self.redis = Redis(host='localhost', port=6379, decode_responses=True)

    async def create_workout_with_schedule(self, workout_schem: WorkoutScheme):
        workout = Workout(
            user_id = workout_schem.user_id,
            name=workout_schem.name,
            description=workout_schem.description,
            rate=workout_schem.rate,
        )

        if workout_schem.training_days:
            for tr_day in workout_schem.training_days:
                training_day = TrainingDay(
                    name=tr_day.name,
                    day_order=tr_day.day_order,
                )

                if tr_day.day_exercises:
                    for day_ex in tr_day.day_exercises:
                        day_exercise = DayExercise(
                            exercises_id=day_ex.exercise_id,
                            exercise_order=day_ex.exercise_order,
                            sets=day_ex.sets,
                            reps=day_ex.reps
                        )
                        training_day.day_exercises.append(day_exercise)

                workout.training_days.append(training_day)
                
        return await self.workoutrepo.create_workout_with_schedule(workout=workout)
        