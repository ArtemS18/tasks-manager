from typing import Annotated

from fastapi import Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.depends.services import (
    ConfirmEmailServiceDepends,
    LoginServiceDepends,
)
from app.auth.schemas.token import RefreshTokenRequest
from app.auth.schemas.auth import ConfirmEmailSchema, UserCredentials
from app.auth.schemas.users import User


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def validation_refresh_token(
    data: Annotated[RefreshTokenRequest, Body()],
    service: LoginServiceDepends,
):
    if data.refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access token required. Please provide the 'refresh_token'.",
        )
    user = await service.validation_user(data.refresh_token)
    await service.validation_refresh_token(user, data.refresh_token)
    return user


async def validation_confirm_token(
    data: Annotated[ConfirmEmailSchema, Body()],
    service: ConfirmEmailServiceDepends,
):
    if data.confirm_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access token required. Please provide the 'confirm_token'",
        )
    user = await service.validation_confirming_token(data.confirm_token)
    return UserCredentials(user=user, data=data)


ValidateConfirmToken = Annotated[User, validation_confirm_token]
ValidateAccessToken = Annotated[str, Depends(oauth2_schema)]
