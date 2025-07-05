from datetime import datetime, timezone
import logging
from fastapi import HTTPException, status
from app.store.bd.models.users_models import RefreshToken
from app.store.bd.repository.user import UserRepository
from app.entity.dto import CreateUserDTO
from app.entity.user import User
from app.service.auth.jwt import JwtService
from app.service.auth.password import verify_password, hash_password_async, create_confirm_password
from app.store.redis.accessor import RedisAccessor
from app.store.bd.models.users_models import UserStatus
from app.web.exception import FORBIDDEN, UNAUTHORIZE
from app.web.utils import async_time

logger = logging.getLogger(__name__)

class LoginService:
    def __init__(self, repository, jwt, redis):
        self.repository: UserRepository = repository
        self.jwt: JwtService = jwt
        self.redis: RedisAccessor = redis
        
    async def authentication_email(self, email:str)->User:
        user = await self.repository.get_user(email)
        if user is None:
            raise UNAUTHORIZE
        return User.model_validate(user)
        
    def authentication_password(self, password:str, hashed_password: str):
        if not verify_password(str(password), str(hashed_password)):
            raise UNAUTHORIZE

    async def authentication(self, form_data)->User:
        user: User = await self.authentication_email(form_data.login)
        if user.status != UserStatus.active:
            raise FORBIDDEN
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
    @async_time
    async def create_confirm_token(self, user: User):
        payload = {
            "sub": user.login,
            "id": user.id,
            "for_confirm": 1
        }
        token = self.jwt.create_confirm_token(payload)
        return token
    
    async def create_refresh_token(self, user: User):
        payload = {
            "sub": user.login,
            "id": user.id
        } 
        refresh = self.jwt.create_refresh_token(payload)
        await self.repository.create_refresh_token(refresh.token, refresh.expire, user.id)
        return refresh.token
    
    @async_time
    async def create_confirming_password(self, user: User) -> None:
        password = create_confirm_password()
        logger.info(password)
        await self.redis.create_confirming_password(user.id, password)

    async def validation_user(self, token:str):
        payload = self.jwt.verify_token(token)
        email = payload.get('sub')
        user = await self.authentication_email(email)
        return user
    
    async def validation_user_for_confirm(self, token:str):
        payload = self.jwt.verify_token(token)
        email = payload.get('sub')
        if payload.get('for_confirm') != 1:
            raise HTTPException(status_code=401, detail="Bad confirm token")
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
    @async_time
    async def register_user(self, new_user: CreateUserDTO):
        if await self.repository.get_user(new_user.login):
            raise HTTPException(status_code=409, detail="Email address already registered.")
        new_user.password = await hash_password_async(new_user.password)
        user = await self.repository.create_user(new_user)
        return User.model_validate(user)
    
    async def confirm_email(self, user: User, user_password: str):
        logger.debug(f"Start confirm email {user.login}")
        password = await self.redis.get_confirming_password(user.id)
        if password is None:
            raise HTTPException(status_code=401, detail="User not found")
        if password != user_password:
            raise HTTPException(status_code=401, detail="Not valid password")
        user = await self.repository.update_user(user.id, status=UserStatus.active.name)
        return user
        





        
