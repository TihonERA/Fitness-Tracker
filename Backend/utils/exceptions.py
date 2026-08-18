from abc import ABC, abstractmethod
from typing import NoReturn

from sqlalchemy.exc import IntegrityError


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
        self.status_code = 400
        self.detail = detail
        super().__init__(detail)

class Conflict(Exception):
    def __init__(self, detail: str) -> None:
        self.status_code = 409
        self.detail = detail
        super().__init__(detail)

class Forbidden(Exception):
    def __init__(self, detail: str = "Access defnied") -> None:
        self.status_code = 403
        self.detail = detail
        super().__init__(detail)

class DBSchemaMismatchError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail

class PostgreSQLStateStrategy(ABC):
    @abstractmethod
    def raise_exception(self, orig_error) -> None:
        pass

class UniqueViolationStrategy(PostgreSQLStateStrategy):
    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail 

    def raise_exception(self, orig_error) -> None:
        if self.detail:
            raise Conflict(detail=self.detail)

        err_dict = orig_error.__cause__.__dict__
        table_name = err_dict.get('table', 'Record')   

        raise Conflict(detail=f"{table_name} with this data already exists")

class ForeignKeyViolationStrategy(PostgreSQLStateStrategy):
    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail

    def raise_exception(self, orig_error) -> None:
        if self.detail:
            raise NotFound(detail=self.detail)

        err_dict = orig_error.__cause__.__dict__
        table_name = err_dict.get('table', 'Record')   

        raise NotFound(detail=f"The referenced {table_name} was not found")

class NotNullViolationStrategy(PostgreSQLStateStrategy):
    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail

    def raise_exception(self, orig_error) -> None:
        if self.detail:
            raise BadRequest(detail=self.detail)

        err_dict = orig_error.__cause__.__dict__
        table_name = err_dict.get('table', 'Record')   
        column = err_dict.get('column', 'Not found')  

        raise BadRequest(detail=f"A required field {column} is missing")

class DBErrorHandler:
    @staticmethod
    def handle_integrity_error(e: IntegrityError, detail: str | None = None) -> NoReturn:
        sqlstate = getattr(e.orig, "sqlstate", None)

        if sqlstate is None:
            raise InternalServerError(detail=str(e))

        strategies: dict[str, PostgreSQLStateStrategy] = {
            "23505": UniqueViolationStrategy(detail=detail),
            "23503": ForeignKeyViolationStrategy(detail=detail),
            "23502": NotNullViolationStrategy(detail=detail)
        }

        strategy = strategies.get(sqlstate) 

        if strategy:
            strategy.raise_exception(e.orig)

        raise InternalServerError(detail=str(e))
