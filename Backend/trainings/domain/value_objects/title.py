from dataclasses import dataclass

from Backend.trainings.domain.exceptions.workout_exceptions import TitleError


@dataclass(frozen=True)
class EntityTitle:
    value: str

    def __post_init__(self) -> None:
        cleaned = self.value.strip()
        length = len(cleaned)
        if not (1 <= length <= 100):
            raise TitleError(length)

        object.__setattr__(self, "value", cleaned)
