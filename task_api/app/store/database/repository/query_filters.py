from sqlalchemy import Select, and_, exists, not_, or_, select
from app.projects.models.member import Assign, Member
from app.projects.models.tasks import Comment, Task
from app.projects.schemas.filters import BaseFilters, CommentsFilters, MembersFilters


def add_base_filters(query: Select, filters: BaseFilters):
    query = query.limit(filters.limit).offset(filters.offset)
    return query


def add_comment_filters(query: Select, filters: CommentsFilters):
    if filters.author_id is not None:
        query = query.where(Comment.author_id == filters.author_id)
    query = add_base_filters(query, filters)
    return query


def add_members_filters(query: Select, filters: MembersFilters):
    assign = select(Assign.id).where((Assign.member_id == Member.id))
    author = select(Task.id).where((Task.author_id == Member.id))

    if filters.task_id is not None:
        assign = select(Assign.id).where(
            and_(Assign.member_id == Member.id, Assign.task_id == filters.task_id)
        )
        author = select(Task.id).where(
            and_(Task.author_id == Member.id, Task.id == filters.task_id)
        )

    if filters.is_assigned and filters.is_author:
        query = query.where(or_(exists(assign), exists(author)))
    else:
        if filters.is_assigned is True:
            query = query.where(exists(assign))
        elif filters.is_assigned is False:
            query = query.where(not_(exists(assign)))
        if filters.is_author is True:
            query = query.where(exists(author))
        elif filters.is_author is False:
            query = query.where(not_(exists(author)))

    if filters.role is not None:
        query = query.where(Member.role == filters.role)
    if filters.status is not None:
        query = query.where(Member.status == filters.status)

    query = add_base_filters(query, filters)
    return query
