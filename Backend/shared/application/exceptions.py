class ApplicationError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
