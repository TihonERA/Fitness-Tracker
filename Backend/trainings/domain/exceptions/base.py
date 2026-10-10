class DomainError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class TitleError(DomainError):
    def __init__(self, name_length: int) -> None:
        super().__init__(f"Name's length must be between 1 and 100, got {name_length}")
