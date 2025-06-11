from fastapi import HTTPException, status
from app.entity.user import User
from app.service.authentication.password import verify_password
from app.service.jwt.utils import JwtService
from app.web.config import get_config

class LoginService:
    def __init__(self, repository):
        self.repository = repository
        self.jwt = JwtService(get_config())
        self.unauthorized_exec = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user", 
            headers={"WWW-Authenticate": "Bearer"})
        
    async def authentication_email(self, email:str)->User:
        user = await self.repository.get_user(email)
        if user is None:
            raise self.unauthorized_exec
        return User.model_validate(user)
        
    def authentication_password(self, password:str, hashed_password: str):
        if not verify_password(password, hashed_password):
            raise self.unauthorized_exec

    async def authentication(self, form_data)->User:
        user:User = await self.authentication_email(form_data.email)
        self.authentication_password(form_data.password, user.hashed_password)
        return user
       
    async def create_access_token(self, user: User):
        payload = {
            "sub": user.login,
            "name": user.name
        }
        token = self.jwt.create_token(payload)
        return token

    async def validation_user(self, token:str):
        email = self.jwt.verify_token(token)
        user = await self.authentication_email(email)
        return user





        
