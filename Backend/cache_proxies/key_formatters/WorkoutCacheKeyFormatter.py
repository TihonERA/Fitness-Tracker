from uuid import UUID

from Backend.cache_proxies.key_formatters.BaseCacheKeyFormatter import BaseCacheKeyFormatter
from Backend.schemas.workout import WorkoutCachePrefixes, WorkoutGetAllFilterDTO


class WorkoutCacheKeyFormatter(BaseCacheKeyFormatter):
    def __init__(self):
        self.pref = WorkoutCachePrefixes

    def get_loaded_workout_key(
        self,
        workout_id: int
    ) -> str:
        return self.formate_key(
            prefix=self.pref.loaded_workout,
            workout_id=workout_id
        )

    def get_workouts_version_key(self, target_user_id: UUID | None) -> str:
        return self.formate_key(
            prefix=self.pref.version,
            user_id=target_user_id
        )

    def get_all_workouts_key(self, version: str, data: WorkoutGetAllFilterDTO) -> str:
        return self.formate_key(
            prefix=self.pref.all_workouts,
            version=version,
            data=data.model_dump()
        )

