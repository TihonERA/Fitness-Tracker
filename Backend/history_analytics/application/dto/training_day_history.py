from dataclasses import dataclass


@dataclass(frozen=True)
class CreateTrainingDayHistoryCommand:
    day_id: int
    day_name: str
