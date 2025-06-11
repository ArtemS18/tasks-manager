from typing import Annotated
from fastapi import APIRouter, Depends, Form, Response

from app.api.depencies import login_service
from app.api.authorization.schemas import TokenResponseSchema, AuthorizationRequestSchema
from app.service.authentication.login import LoginService
from app.service.cookies.utils import set_cookie

router = APIRouter(prefix="/login", tags=["Autorization"])

@router.post("/", response_model=TokenResponseSchema)
async def login_user(response: Response, service:Annotated[LoginService, Depends(login_service)], form_data:Annotated[AuthorizationRequestSchema, Form()]):
    user = await service.authentication(form_data)
    token = await service.create_access_token(user)
    set_cookie(response, key="access_token", value=token)
    return TokenResponseSchema(access_token=token, token_type="Bearer").model_dump()