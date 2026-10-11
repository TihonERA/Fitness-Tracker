from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from Backend.analytics.domain.sets_history import SetsHistory


@dataclass
class ExerciseHistory:
    id: int
    user_id: UUID
    exercise_id: int
    training_day_history_id: int | None
    created_at: datetime
    sets_history: list[SetsHistory]
