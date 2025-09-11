from typing import Annotated

from fastapi import Cookie, HTTPException, status, Depends

from app.auth.controllers.confirm import ConfirmEmailService
from app.auth.controllers.login import LoginService
from app.auth.controllers.jwt import JwtService
from app.lib.fastapi import Request


def jwt_service(req: Request) -> JwtService:
    return JwtService(req.app.config)


def login_service(req: Request, auth=Depends(jwt_service)):
    print(vars(req.app.store.repo.user))
    print(req.app.store.repo.user.get_user_by_email)
    return LoginService(
        config=req.app.config, repository=req.app.store.repo.user, jwt=auth
    )


def confirm_email_service(
    req: Request, jwt=Depends(jwt_service)
) -> ConfirmEmailService:
    store = req.app.store
    return ConfirmEmailService(
        req.app.config, store.broker, store.repo.user, store.redis, jwt
    )


LoginServiceDepends = Annotated[LoginService, Depends(login_service)]

ConfirmEmailServiceDepends = Annotated[
    ConfirmEmailService, Depends(confirm_email_service)
]
