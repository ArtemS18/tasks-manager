import logging
from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, Response

from app.auth.depends.services import (
    ConfirmEmailServiceDepends,
    LoginServiceDepends,
)
from app.auth.depends.validations import (
    validation_confirm_token,
    validation_refresh_token,
)
from app.auth.schemas.auth import (
    AuthoSchema,
    RegisterSchema,
    UserCredentials,
)
from app.auth.schemas.token import (
    AccessAndRefreshTokenResponse,
    ConfirmTokenResponse,
    TokenResponse,
)
from app.auth.schemas.users import UserSchemaResponse, User
from app.lib.shemas import OKResponseSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Autorization"])


@router.post("/token")
async def login_user(
    service: LoginServiceDepends,
    form_data: Annotated[AuthoSchema, Form()],
) -> AccessAndRefreshTokenResponse:
    user = await service.authorizition_user(form_data)
    access_token = await service.create_access_token(user)
    refresh_token = await service.create_refresh_token(user)

    return AccessAndRefreshTokenResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/reg", summary="Create user and notice code from email")
async def reg_user(
    form_data: Annotated[RegisterSchema, Body()],
    auth_service: LoginServiceDepends,
    cofirm_service: ConfirmEmailServiceDepends,
) -> ConfirmTokenResponse:
    user = await auth_service.register_user(form_data)

    token = await cofirm_service.send_email_and_get_confirming_token(user)
    return ConfirmTokenResponse(confirm_token=token)


@router.post("/confirm", response_model=OKResponseSchema, summary="Email verification")
async def confirm_email(
    service: ConfirmEmailServiceDepends,
    form: UserCredentials = Depends(validation_confirm_token),
):
    user = form.user
    await service.confirm_password_from_email(user, form.data.password)
    user_response = UserSchemaResponse.model_validate(user)

    return OKResponseSchema(
        message=f"Email {user.login} confirmed", details=user_response.model_dump()
    )


@router.get("/refresh")
async def get_refresh_token(
    user: Annotated[User, Depends(validation_refresh_token)],
    service: LoginServiceDepends,
) -> TokenResponse:
    token = await service.create_access_token(user)

    return TokenResponse(access_token=token)
