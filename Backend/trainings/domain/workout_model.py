from dataclasses import dataclass
from typing import Any
from uuid import UUID

from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
)
from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass
class Workout:
    id: int | None
    user_id: UUID
    name: EntityTitle
    description: str | None
    public: bool

    @classmethod
    def create(
        cls,
        user_id: UUID,
        name: EntityTitle,
        description: str | None = None,
        public: bool = False,
    ) -> "Workout":
        return cls(
            id=None,
            user_id=user_id,
            name=name,
            description=description,
            public=public,
        )

    def ensure_ownership(self, user_id: UUID) -> None:
        if self.user_id != user_id:
            raise WorkoutAccessDenied()

    def update(
        self,
        name: EntityTitle | None = None,
        description: str | None = None,
        public: bool | None = None,
    ) -> None:
        if name:
            self.name = name

        if description is not None:
            self.description = description

        if public is not None:
            self.public = public
