from typing import Any
from app.entity.base import Base


def json_response(schema: Base, obj: Any):
    return schema.model_validate(obj).model_dump()