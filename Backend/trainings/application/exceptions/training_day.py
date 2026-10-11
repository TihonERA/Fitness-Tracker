from Backend.shared.application.exceptions import ApplicationError


class TrainingDayNotCreatedError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Cant change unexisting entity")


class TrainingDayConcurrencyError(ApplicationError):
    def __init__(self, id: int) -> None:
        super().__init__(
            "Training Day with id: {id} was concurrently deleted or does not exist"
        )
