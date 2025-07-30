from typing import Annotated

from fastapi import Body, Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth.depends.services import (
    ConfirmEmailServiceDepends,
    LoginServiceDepends,
)
from app.auth.schemas.token import RefreshTokenRequest
from app.auth.schemas.auth import ConfirmEmailSchema, UserCredentials
from app.auth.schemas.users import User, UserTokenPayload


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")

ValidateAccessToken = Annotated[str, Depends(oauth2_schema)]


async def validation_refresh_token(
    data: Annotated[RefreshTokenRequest, Cookie()],
    service: LoginServiceDepends,
):
    user = await service.validation_refresh_token(data.refresh_token)
    return user


async def validation_confirm_token(
    data: Annotated[ConfirmEmailSchema, Body()],
    service: ConfirmEmailServiceDepends,
):
    user = await service.validation_confirming_token(data.confirm_token)
    return UserCredentials(user=user, data=data)


async def validation_access_token(
    access_token: ValidateAccessToken,
    service: LoginServiceDepends,
) -> User:
    user = await service.validation_access_token(access_token)
    return user


ValidateConfirmToken = Annotated[UserCredentials, validation_confirm_token]
