from dataclasses import dataclass

from Backend.trainings.domain.exceptions.workout_exceptions import NameException


@dataclass(frozen=True)
class EntityTitle:
    value: str

    def __post_init__(self) -> None:
        cleaned = self.value.strip()
        if len(cleaned) > 100:
            raise NameException()

        object.__setattr__(self, "value", cleaned)
