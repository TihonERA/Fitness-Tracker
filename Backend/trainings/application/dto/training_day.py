from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingDayReadDTO:
    id: int
    workout_id: int
    name: str
    day_order: int
