class NotFound(Exception):
    def __init__(self, detail: str = "Not Found"):
        self.status_code = 404
        self.detail = detail
        super().__init__(detail)

class DataNotModified(Exception):
    def __init__(self, detail: str = "No changes detected"):
        self.status_code = 204
        self.detail = detail
        super().__init__(detail)

class InternalServerError(Exception):
    def __init__(self, detail: str = "Internal server error"):
        self.status_code = 500
        self.detail = detail
        super().__init__(detail)

class InvalidCredentials(Exception):
    def __init__(self, detail: str = "Could not validate credentials") -> None:
        self.status_code = 401
        self.detail = detail
        super().__init__(detail)

class BadRequest(Exception):
    def __init__(self, detail: str = "Bad request") -> None:
        self.detail = detail
        super().__init__(detail)
