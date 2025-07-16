from typing import Annotated
from fastapi import Depends
from app.lib.fastapi import Request
from app.projects.services.members import MemberService
from app.store.database.repository.members import MemberRepository


def get_member_repo(req: Request):
    return req.app.store.repo.member


def get_member_service(
    req: Request, member_repo: MemberRepository = Depends(get_member_repo)
):
    return MemberService(member_repo=member_repo)


MemberServiceDepend = Annotated[MemberService, Depends(get_member_service)]
