from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

NameStr = Annotated[str, Field(max_length=100)]
DescriptionStr = Annotated[str, Field(max_length=2000)]
