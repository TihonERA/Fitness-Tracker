from Backend.history_analytics.models.training_day_history import TrainingDayHistory
from copy import copy

class FakeTrainingDayHistoryRepository:
    def __init__(self) -> None:
        self.db: dict[int, TrainingDayHistory] = {}

    async def create(self, training_day_history: TrainingDayHistory) -> TrainingDayHistory:
        training_day_history_copy = copy(training_day_history)
        training_day_history_copy.id = training_day_history_id

        if len(self.db) == 0:
            training_day_history_id = 1

            self.db[training_day_history_id] = training_day_history_copy

            return copy(training_day_history_copy)

        training_day_history_id = self.db.keys()[-1] + 1
        self.db[training_day_history_id] = training_day_history_copy

        return copy(training_day_history_copy)

        

    
