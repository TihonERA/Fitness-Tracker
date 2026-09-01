from uuid import UUID

from Backend.cache_proxies.key_formatters.BaseCacheKeyFormatter import (
    BaseCacheKeyFormatter,
)
from Backend.schemas.training_day_history import (
    TrainingDayHistoryCachePrefixes,
    TrainingDayHistoryGetAll,
    TrainingDayHistoryGetAllDTO,
)


class TrainingDayHistoryCacheKeyFormatter(BaseCacheKeyFormatter):
    def __init__(self) -> None:
        self.pr = TrainingDayHistoryCachePrefixes

    def get_tag_key(self, user_id: UUID) -> str:
        return self.formate_key(prefix=self.pr.tag, user_id=user_id)

    def get_loaded_key(self, id: int) -> str:
        return self.formate_key(self.pr.get_loaded_key, id=id)

    def get_version_key(self, user_id: UUID) -> str:
        return self.formate_key(self.pr.version, user_id=user_id)

    def get_all_key(self, version: str, data: TrainingDayHistoryGetAllDTO) -> str:
        return self.formate_key(
            prefix=self.pr.get_all_key, version=version, data=data.model_dump()
        )
