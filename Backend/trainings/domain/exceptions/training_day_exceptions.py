from Backend.trainings.domain.exceptions.workout_exceptions import DomainError


class TrainingDayNotFound(DomainError):
    def __init__(self, day_id: int) -> None:
        super().__init__(f"Day with id: {day_id} was not found")


class TrainingDayOrderError(DomainError):
    def __init__(self, day_order: int) -> None:
        super().__init__(f"Day order must be between 1 and 7, got {day_order}")
