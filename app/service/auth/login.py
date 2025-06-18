from datetime import datetime, timezone
import logging
from fastapi import HTTPException, status
from app.bd.models.users_models import RefreshToken
from app.bd.repository.user import UserRepository
from app.entity.dto import CreateUserDTO
from app.entity.user import User
from app.service.auth.jwt import JwtService
from app.service.auth.password import verify_password, hash_password
from app.web.config import get_config

logger = logging.getLogger(__name__)

class LoginService:
    def __init__(self, repository, jwt):
        self.repository: UserRepository = repository
        self.jwt: JwtService = jwt
        self._config = get_config()
        self.unauthorized_exec = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid email or password", 
            headers={"WWW-Authenticate": "Bearer"})
        
    async def authentication_email(self, email:str)->User:
        user = await self.repository.get_user(email)
        if user is None:
            raise self.unauthorized_exec
        return User.model_validate(user)
        
    def authentication_password(self, password:str, hashed_password: str):
        if not verify_password(str(password), str(hashed_password)):
            raise self.unauthorized_exec

    async def authentication(self, form_data)->User:
        user: User = await self.authentication_email(form_data.login)
        self.authentication_password(form_data.password, user.hashed_password)
        return user
       
    async def create_access_token(self, user: User):
        payload = {
            "sub": user.login,
            "id": user.id,
            "name": user.name
        }
        token = self.jwt.create_access_token(payload)
        return token
    
    async def create_refresh_token(self, user: User):
        payload = {
            "sub": user.login,
            "id": user.id
        } 
        refresh = self.jwt.create_refresh_token(payload)
        await self.repository.create_refresh_token(refresh.token, refresh.expire, user.id)
        return refresh.token

    async def validation_user(self, token:str):
        email = self.jwt.verify_token(token)
        user = await self.authentication_email(email)
        return user
    
    async def validation_refresh_token(self, user: User, refresh_token: str):
        token: RefreshToken = await self.repository.get_refresh_token(user.id, refresh_token)
        if token is None:
            raise HTTPException(status_code=403, detail="Authorizate error refresh token")
        if token.blocked:
            raise HTTPException(status_code=403, detail="Authorizate error refresh token is blocked")
        if token.expire_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expire time out")
        logger.info("New refresh token was created for user %s", user.id)
        return token.token
        
    async def register_user(self, new_user: CreateUserDTO):
        if await self.repository.get_user(new_user.login):
            raise HTTPException(status_code=409, detail="Email address already registered.")
        new_user.password = hash_password(new_user.password)
        user = await self.repository.create_user(new_user)
        return User.model_validate(user)
    





        
