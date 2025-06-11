from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    tg_id: int
    name: str
    login: str
    hashed_password: str
    class Config:
        from_attributes = True