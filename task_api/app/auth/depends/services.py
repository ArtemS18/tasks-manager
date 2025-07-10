from typing import Annotated

from fastapi import Cookie, HTTPException, status, Depends

from app.auth.controllers.confirm import ConfirmEmailService
from app.auth.controllers.login import LoginService
from app.auth.controllers.jwt import JwtService
from app.lib.fastapi import Request


def jwt_service(req: Request) -> JwtService:
    return JwtService(req.app.config)


def login_service(req: Request, auth=Depends(jwt_service)):
    return LoginService(repository=req.app.store.user, jwt=auth)


def confirm_email_service(
    req: Request, jwt=Depends(jwt_service)
) -> ConfirmEmailService:
    store = req.app.store
    return ConfirmEmailService(store.broker, store.user, store.redis, jwt)


LoginServiceDepends = Annotated[LoginService, Depends(login_service)]

ConfirmEmailServiceDepends = Annotated[
    ConfirmEmailService, Depends(confirm_email_service)
]
