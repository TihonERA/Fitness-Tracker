from Backend.trainings.domain.exceptions.workout_exceptions import DomainError


class TrainingDayNotFound(DomainError):
    def __init__(self, day_id: int) -> None:
        super().__init__(f"Day with id: {day_id} was not found")


class TrainingDayOrderException(DomainError):
    def __init__(self, day_order: int) -> None:
        self.detail = f"Day order cant be {'less' if day_order < 1 else 'higher'} than {day_order}"
        super().__init__(self.detail)
