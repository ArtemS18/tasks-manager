from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import Field
from app.base.base_pydantic import Base
from app.auth.schemas.users import User


class Message(Base):
    id: Optional[ObjectId] = Field(default=None, alias='_id')
    text: str 
    author: User 
    created_at: datetime = Field(default_factory=datetime.now)
    project_id: int
    chat_id: int
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
     }
