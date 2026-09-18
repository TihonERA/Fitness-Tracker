class DomainError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class WorkoutNotFound(DomainError):
    def __init__(self, workout_id: int | None = None) -> None:
        super().__init__(
            f"Workout with id: {workout_id or 'not created instance'} was not found"
        )


class TitleError(DomainError):
    def __init__(self, name_length: int) -> None:
        super().__init__(f"Name's length must be between 0 and 100, got {name_length}")


class WorkoutAccessDenied(DomainError):
    def __init__(self) -> None:
        super().__init__(f"Access to this workout was denied")


class DayExerciseNotFound(DomainError):
    def __init__(self, day_id: int, exercise_id: int) -> None:
        super().__init__(
            f"Exercise with id: {exercise_id} was not found in day with id {day_id}"
        )
