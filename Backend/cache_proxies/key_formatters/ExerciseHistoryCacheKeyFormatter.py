from uuid import UUID

from Backend.cache_proxies.key_formatters.BaseCacheKeyFormatter import (
    BaseCacheKeyFormatter,
)
from Backend.schemas.exercise_history import (
    ExerciseHistoryCachePrefixes,
    ExerciseHistoryGetAllDTO,
)


class ExerciseHistoryCacheKeyFormatter(BaseCacheKeyFormatter):
    def __init__(self) -> None:
        self.pr = ExerciseHistoryCachePrefixes

    def get_loaded_key(self, history_id) -> str:
        return self.formate_key(prefix=self.pr.loaded, id=history_id)

    def get_all_key(self, data: ExerciseHistoryGetAllDTO) -> str:
        return self.formate_key(prefix=self.pr.all, data=data.model_dump())

    def get_tag_key(self, user_id: UUID) -> str:
        return self.formate_key(self.pr.tag, user_id=user_id)

    def get_version_key(self, user_id: UUID) -> str:
        return self.formate_key(self.pr.version, user_id=user_id)
