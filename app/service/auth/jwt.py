import jwt
from typing import Dict
from datetime import datetime, timezone, timedelta

from app.entity.token import RefreshTokenDTO
from app.web.config import BaseConfig
from app.web.exception import UNAUTHORIZE

class JwtService:
    def __init__(self, config: BaseConfig):
        self._config: BaseConfig = config

    def create_access_token(
            self,
            payload: Dict,
            expire: int | None = None,
            expire_at: datetime | None = None
    ):
        if self._config is None:
            raise ValueError("JwtService must be initialized with a config object.")

        now = datetime.now(timezone.utc)
        encode = payload.copy()
        if expire_at is None:
            encode.update(
                {"exp": now + timedelta(minutes=expire) if expire else now + timedelta(minutes=self._config.JWT_EXPIRE_MINUTES)}
            )
        else:
            encode.update(
                {"exp": expire_at}
            )
        access_token = jwt.encode(
            encode,
            self._config.JWT_SECRET_KEY,
            self._config.JWT_ALGORIM
        )
        return access_token

    def verify_token(self,token: str):
        if self._config is None:
            raise ValueError("JwtService must be initialized with a config object.")

        unautorized_exc = UNAUTHORIZE
        try:
            payload = jwt.decode(
                token, 
                self._config.JWT_SECRET_KEY, 
                self._config.JWT_ALGORIM
        )
        except jwt.PyJWTError:
            unautorized_exc.detail = "Expire time out"
            raise unautorized_exc
        email = payload.get('sub')
        if not email:
            unautorized_exc.detail = "Not valid token"
            raise unautorized_exc
        return email
    
    def create_refresh_token(self, payload: Dict, expire: int|None= None):
        now = datetime.now(timezone.utc)
        expire_time = expire if expire else self._config.JWT_REFRESH_EXPIRE_HOURS
        expire_at = now+timedelta(expire_time)

        token = self.create_access_token(payload=payload, expire_at=expire_at)
        return RefreshTokenDTO(token=token, expire=expire_at)
