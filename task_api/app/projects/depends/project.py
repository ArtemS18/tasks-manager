from typing import Annotated

from fastapi import Depends, Path
from app.lib.fastapi import Request
from app.projects.services.project import ProjectService
from app.store.broker.accessor import BrokerAccessor


def get_project_id(project_id: int = Path(...)) -> int:
    return project_id


def get_project_service(req: Request):
    return ProjectService(
        req.app.store.repo.project, req.app.store.repo.user, req.app.store.repo.member
    )


def broker_service(req: Request):
    return req.app.store.broker


ProjectServiceDepend = Annotated[ProjectService, Depends(get_project_service)]
ProjectId = Annotated[int, Depends(get_project_id)]
BrokerAccessorDepend = Annotated[BrokerAccessor, Depends(broker_service)]
