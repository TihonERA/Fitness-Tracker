from uuid import UUID

from Backend.cache_proxies.key_formatters.BaseCacheKeyFormatter import BaseCacheKeyFormatter
from Backend.schemas.user import UserCachePrefixes


class UserCacheKeyFormatter(BaseCacheKeyFormatter):
    def __init__(self):
        self.pref = UserCachePrefixes

    def get_user_by_id_key(self, user_id: UUID) -> str:
        return self.formate_key(
            prefix=self.pref.user_by_id,
            user_id=user_id
        )
    
    def get_user_by_login_key(self, login: str) -> str:
        return self.formate_key(
            prefix=self.pref.user_by_login,
            login=login
        )

    def get_user_by_email_key(self, email: str) -> str:
        return self.formate_key(
            prefix=self.pref.user_by_email,
            email=email
        )

    def get_tag_key(self, user_id: UUID) -> str:
        return self.formate_key(
            prefix=self.pref.tag_user,
            user_id=user_id
        )
 

