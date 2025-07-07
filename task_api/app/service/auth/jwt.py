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
        expire_at: datetime | None = None,
    ):
        if self._config is None:
            raise ValueError("JwtService must be initialized with a config object.")

        now = datetime.now(timezone.utc)
        encode = payload.copy()
        if expire_at is None:
            encode.update(
                {
                    "exp": now + timedelta(minutes=expire)
                    if expire
                    else now + timedelta(minutes=self._config.jwt.access_expire)
                }
            )
        else:
            encode.update({"exp": expire_at})
        access_token = jwt.encode(
            encode, self._config.jwt.secret_key, self._config.jwt.algorithm
        )
        return access_token

    def verify_token(self, token: str) -> dict:
        if self._config is None:
            raise ValueError("JwtService must be initialized with a config object.")

        unautorized_exc = UNAUTHORIZE
        try:
            payload = jwt.decode(
                token, self._config.jwt.secret_key, self._config.jwt.algorithm
            )
        except jwt.PyJWTError:
            unautorized_exc.detail = "Expire time out"
            raise unautorized_exc
        sub = payload.get("sub")
        if not sub:
            unautorized_exc.detail = "Not valid token"
            raise unautorized_exc
        return payload

    def create_refresh_token(self, payload: Dict, expire: int | None = None):
        now = datetime.now(timezone.utc)
        expire_time = expire if expire else self._config.jwt.refresh_expire
        expire_at = now + timedelta(expire_time)

        token = self.create_access_token(payload=payload, expire_at=expire_at)
        return RefreshTokenDTO(token=token, expire=expire_at)

    def create_confirm_token(self, payload: Dict, expire: int | None = None):
        return self.create_access_token(
            payload=payload, expire=self._config.jwt.confirm_expire
        )
