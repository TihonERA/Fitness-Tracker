from Backend.analytics.domain.training_day_history import TrainingDayHistory
from Backend.analytics.infrastructure.models.training_day_history import (
    TrainingDayHistoryModel,
)


class TrainingDayHistoryMapper:
    @staticmethod
    def to_domain(
        training_day_history_model: TrainingDayHistoryModel,
    ) -> TrainingDayHistory:
        return TrainingDayHistory(
            id=training_day_history_model.id,
            day_id=training_day_history_model.day_id,
            day_name=training_day_history_model.day_name,
            created_at=training_day_history_model.created_at,
        )

    @staticmethod
    def to_orm(training_day_history: TrainingDayHistory) -> TrainingDayHistoryModel:
        return TrainingDayHistoryModel(
            day_id=training_day_history.day_id,
            day_name=training_day_history.day_name,
            created_at=training_day_history.created_at,
        )
