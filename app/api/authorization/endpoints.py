from typing import Annotated
from fastapi import APIRouter, Depends, Form, Response, BackgroundTasks

from app.api.depencies import login_service, smtp_client, validation_refresh_token
from app.api.authorization.schemas import OKResponseSchema, AuthorizationRequestSchema, RegisterUserSchema, UserSchemaResponse
from app.email.send_email import SmtpClient
from app.entity.user import User
from app.service.auth.login import LoginService
from app.service.utils import set_cookie

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
    service:Annotated[LoginService, Depends(login_service)], 
    form_data:RegisterUserSchema,
    smtp_client: Annotated[SmtpClient, Depends(smtp_client)],
    background_tasks: BackgroundTasks
):
    user = await service.register_user(form_data)

    background_tasks.add_task(smtp_client.send_email, user_id=user.id)
    user_response = UserSchemaResponse.model_validate(user)
    return OKResponseSchema(message="Success registered user", details=user_response.model_dump())

@router.get("/refresh", response_model=OKResponseSchema)
async def get_refresh_token(
    response: Response, 
    user: Annotated[User, Depends(validation_refresh_token)],
    service: Annotated[LoginService, Depends(login_service)]
):
    token = await service.create_access_token(user)
    set_cookie(response, key="access_token", value=token)
    return OKResponseSchema(message="Success created new access token")