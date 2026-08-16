from Backend.cache_proxies.key_formatters.BaseCacheKeyFormatter import BaseCacheKeyFormatter
from Backend.schemas.training_day import TrainingDayCachePrefixes

class TrainingDayCacheKeyFormatter(BaseCacheKeyFormatter):
    def __init__(self):
        self.pref = TrainingDayCachePrefixes

    def get_loaded_tr_day_key(self, day_id: int) -> str:
        return self.formate_key(
            prefix=self.pref.loaded_training_day,
            day_id=day_id
        )

