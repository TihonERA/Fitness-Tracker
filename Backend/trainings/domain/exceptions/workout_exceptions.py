class DomainError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class WorkoutNotFound(DomainError):
    def __init__(self, workout_id: int) -> None:
        super().__init__(f"Workout with id: {workout_id} was not found")


class TrainingDayNotFound(DomainError):
    def __init__(self, day_id: int) -> None:
        super().__init__(f"Day with id: {day_id} was not found")


class DayExerciseNotFound(DomainError):
    def __init__(self, day_id: int, exercise_id: int) -> None:
        super().__init__(
            f"Exercise with id: {exercise_id} was not found in day with id {day_id}"
        )
