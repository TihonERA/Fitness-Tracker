from typing import Any


class CacheKeyFormatter:
    def _return_formated_cache_parts(
        self,
        data: dict[str, Any]
    ) -> list[str]:
        parts = []
        for key, value in sorted(data.items()):
            if isinstance(value, dict):
                nested_parts = self._return_formated_cache_parts(value)
                parts.extend(nested_parts)
            else:
                parts.append(f"{key.replace(' ', '')}={value}")

        return parts

    def formate_key(
        self,
        prefix: str,
        **identifiers
    ) -> str:
        cache_parts = self._return_formated_cache_parts(data=identifiers)

        return f"{prefix}:{':'.join(cache_parts)}"
