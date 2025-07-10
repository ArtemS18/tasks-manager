from fastapi import HTTPException, status
from app.lib.fastapi import Request


async def validation_internal_token(
    req: Request,
):
    token = req.headers.get("X-Internal-Token")
    if token is None or token != req.app.config.internal.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )

    return token
