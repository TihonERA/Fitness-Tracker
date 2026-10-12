from dataclasses import dataclass
from datetime import datetime

from Backend.shared.domain.value_objects.entity_title import EntityTitle


@dataclass
class TrainingDayHistory:
    id: int | None
    day_id: int
    day_name: EntityTitle
    created_at: datetime | None

    @classmethod
    def create(cls, day_id: int, day_name: EntityTitle) -> "TrainingDayHistory":
        return cls(id=None, day_id=day_id, day_name=day_name, created_at=None)
