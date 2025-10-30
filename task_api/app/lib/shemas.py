from typing import Any, Optional
from pydantic import BaseModel


class OKResponseSchema(BaseModel):
    message: str
    details: Any | None = None


class PartialModel(BaseModel):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for arg, ann in cls.__annotations__.items():
            cls.__annotations__[arg] = Optional[ann]
            cls.__setattr__(cls.self, arg, None)
