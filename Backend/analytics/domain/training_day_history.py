from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrainingDayHistory:
    id: int
    day_id: int
    day_name: str
    created_at: datetime
