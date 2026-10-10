from Backend.trainings.domain.exceptions.base import DomainError


class TrainingDayNotFound(DomainError):
    def __init__(self, day_id: int | None = None) -> None:
        super().__init__(
            f"Day with id: {day_id or 'not_created_instance'} was not found"
        )


class TrainingDayOrderError(DomainError):
    def __init__(self, day_order: int) -> None:
        super().__init__(f"Day order must be between 1 and 7, got {day_order}")


class TrainingDayAccessDenied(DomainError):
    def __init__(self) -> None:
        super().__init__(f"Access to this training_day was denied")


class DayExerciseNotFound(DomainError):
    def __init__(self, exercise_id: int) -> None:
        super().__init__(f"TrainingDay dont contain exercise with id: {exercise_id}")


class DayExerciseOrderIntegrityError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
