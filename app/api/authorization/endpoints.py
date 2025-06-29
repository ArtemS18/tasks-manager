from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, Response, BackgroundTasks

from app.api.depencies import login_service, validation_confirm_token, validation_refresh_token
from app.api.authorization.schemas import ConfirmEmailSchema, OKResponseSchema, AuthorizationRequestSchema, RegisterUserSchema, UserSchemaResponse
from app.entity.user import User
from app.service.auth.login import LoginService
from app.service.utils import set_cookie
from app.store.broker.tasks import send_autho_email_task

router = APIRouter(prefix="/auth", tags=["Autorization"])

@router.post("/", response_model=OKResponseSchema)
async def login_user(
    response: Response,
    service:Annotated[LoginService, Depends(login_service)], 
    form_data:Annotated[AuthorizationRequestSchema, Form()]
):
    user = await service.authentication(form_data)
    access_token = await service.create_access_token(user)
    refresh_token = await service.create_refresh_token(user)

    set_cookie(response, key="access_token", value=access_token)
    set_cookie(response, key="refresh_token", value=refresh_token)

    return OKResponseSchema(message="Success authotizeted user")

@router.post("/reg", response_model=OKResponseSchema)
async def reg_user(
    response: Response,
    service:Annotated[LoginService, Depends(login_service)], 
    form_data: Annotated[RegisterUserSchema, Body()],
):
    user = await service.register_user(form_data)

    await service.create_confirming_password(user)
    await send_autho_email_task.kiq(user.id)

    confirm_token = await service.create_access_token(user, for_confirm=True)
    set_cookie(response, key="confirm_token", value=confirm_token)

    user_response = UserSchemaResponse.model_validate(user)
    
    return OKResponseSchema(message="Please confirm yout email (login)", details=user_response.model_dump())

@router.post("/confirm", response_model=OKResponseSchema)
async def confirm_email(
    service: Annotated[LoginService, Depends(login_service)],
    data: Annotated[ConfirmEmailSchema, Body()],
    user = Depends(validation_confirm_token)
):
    await service.confirm_email(user, data.password)
    user_response = UserSchemaResponse.model_validate(user)
    return OKResponseSchema(message=f"Email {user.login} confirmed", details=user_response.model_dump())


@router.get("/refresh", response_model=OKResponseSchema)
async def get_refresh_token(
    response: Response, 
    user: Annotated[User, Depends(validation_refresh_token)],
    service: Annotated[LoginService, Depends(login_service)]
):
    token = await service.create_access_token(user)
    set_cookie(response, key="access_token", value=token)
    return OKResponseSchema(message="Success created new access token")