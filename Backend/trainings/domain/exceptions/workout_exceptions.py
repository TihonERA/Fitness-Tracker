from Backend.shared.domain.exceptions import DomainError


class WorkoutNotFound(DomainError):
    def __init__(self, workout_id: int | None = None) -> None:
        super().__init__(
            f"Workout with id: {workout_id or 'not created instance'} was not found"
        )


class WorkoutAccessDenied(DomainError):
    def __init__(self) -> None:
        super().__init__(f"Access to this workout was denied")
