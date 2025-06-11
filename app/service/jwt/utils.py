from typing import Dict
from fastapi import HTTPException, status
import jwt
from datetime import datetime, timezone, timedelta

from app.web.config import BaseConfig

class JwtService:
    def __init__(self, config):
        self._config: BaseConfig = config

    def create_token(
            self,
            payload: Dict,
            expire: int | None = None
    ):
        if self._config is None:
            raise ValueError("JwtService must be initialized with a config object.")

        now = datetime.now(timezone.utc)
        encode = payload.copy()
        encode["exp"] = now + timedelta(minutes=expire) if expire else now + timedelta(minutes=self._config.JWT_EXPIRE_MINUTES)
        access_token = jwt.encode(
            encode,
            self._config.JWT_SECRET_KEY,
            self._config.JWT_ALGORIM
        )
        return access_token

    def verify_token(self,token: str):
        if self._config is None:
            raise ValueError("JwtService must be initialized with a config object.")

        unautorized_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(
                token, 
                self._config.JWT_SECRET_KEY, 
                self._config.JWT_ALGORIM
        )
        except jwt.PyJWTError:
            raise unautorized_exc
        email = payload.get('sub')
        if not email:
            raise unautorized_exc
        return email
