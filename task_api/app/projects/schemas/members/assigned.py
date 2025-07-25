from app.base.base_pydantic import Base


class CreateAssignedSchema(Base):
    member_id: int


class AssignedResponseSchema(Base):  # TODO: сделать нормальный респонс
    task_id: int
    member_id: int
