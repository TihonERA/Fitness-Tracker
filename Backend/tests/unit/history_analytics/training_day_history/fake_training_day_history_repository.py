from Backend.history_analytics.domain.training_day_history import TrainingDayHistory
from copy import copy

class FakeTrainingDayHistoryRepository:
    def __init__(self) -> None:
        self.db: dict[int, TrainingDayHistory] = {}

    async def create(self, training_day_history: TrainingDayHistory) -> TrainingDayHistory:
        training_day_history_id = 0 if len(self.db) else list(self.db.keys())[-1] + 1

        training_day_history_copy = copy(training_day_history)
        training_day_history_copy.id = training_day_history_id

        self.db[training_day_history_id] = training_day_history_copy

        return copy(training_day_history_copy)
