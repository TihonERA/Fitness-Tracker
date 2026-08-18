from datetime import datetime
from typing import Any
from pydantic import AfterValidator, BaseModel, ConfigDict, Field
from typing import Annotated

Str100 = Annotated[str, Field(max_length=100)]
StrText = Annotated[str, Field(max_length=2000)]
SkipInt = Annotated[int, Field(0, ge=0)]
LimitInt = Annotated[int, Field(20, gt=0, le=100)]
OptionalInt = int | None
OptionalDateTime = datetime | None

def validate_password(value: Str100) -> Str100:
    if len(value) <= 12:
        raise ValueError("Password must contain atleast 12 symbols")
    elif len(value) >= 128:
        raise ValueError("Password must be less then 128 symbols")
    return value

Password = Annotated[Str100, AfterValidator(validate_password)]

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Any


