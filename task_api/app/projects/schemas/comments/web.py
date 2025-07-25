from typing import List
from app.base.base_pydantic import Base
from app.projects.schemas.members.web import ShortMemberResponse
from app.projects.models.tasks import Comment as CommentORM
from app.projects.schemas.tasks.dto import Task


class CommentResponseSchema(Base):
    id: int
    task: Task
    text: str
    author: ShortMemberResponse

    @classmethod
    def orm_comment_validate(cls, orm_comment: CommentORM) -> "CommentResponseSchema":
        return cls(
            id=orm_comment.id,
            task=Task.model_validate(orm_comment.task),
            text=orm_comment.text,
            author=ShortMemberResponse.orm_member_validate(orm_comment.author),
        )


class CommentsResponseSchema(Base):
    comments: List[CommentResponseSchema]
