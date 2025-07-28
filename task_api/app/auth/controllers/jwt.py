import logging
import jwt
from typing import Dict
from datetime import datetime, timezone, timedelta
from app.web.config import BaseConfig
from app.web import exception

log = logging.getLogger(__name__)


class JwtService:
    def __init__(self, config: BaseConfig):
        self._config: BaseConfig = config

    def create_token(
        self,
        payload: Dict,
        expire: int | None = None,
        expire_at: datetime | None = None,
    ):
        now = datetime.now(timezone.utc)
        encode = payload.copy()
        if not encode.get("token_type"):
            encode.update({"token_type": "access"})
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
        token = jwt.encode(
            encode, self._config.jwt.secret_key, self._config.jwt.algorithm
        )
        return token

    def verify_token(self, token: str) -> dict:
        try:
            payload: dict = jwt.decode(
                token, self._config.jwt.secret_key, self._config.jwt.algorithm
            )
        except jwt.ExpiredSignatureError:
            raise exception.JWT_TOKEN_EXPIRED
        except jwt.InvalidTokenError:
            raise exception.JWT_BASE_EXEPTION
        except jwt.DecodeError:
            raise exception.JWT_DECODE_ERROR
        if not payload.get("sub") or not payload.get("token_type"):
            raise exception.JWT_BAD_CREDENSIALS
        return payload
