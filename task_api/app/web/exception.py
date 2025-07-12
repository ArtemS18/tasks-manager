from fastapi import HTTPException, status


JWT_MISSING_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Missing token",
    headers={"WWW-Authenticate": "Bearer"},
)

JWT_BASE_EXEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

JWT_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)
JWT_BAD_CREDENSIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)

JWT_DECODE_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Decode error",
    headers={"WWW-Authenticate": "Bearer"},
)

REFRESH_TOKEN_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token not found",
    headers={"WWW-Authenticate": "Bearer"},
)
ACCESS_TOKEN_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token not found",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found",
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_CODE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid confirmation code",
)

INVALID_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid username or password",
)

INVALID_DATA = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data for writing"
)
BD_ERROR_UNIQUE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Its item already existing"
)

FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User has blocked or not confirmed email",
)

TASK_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found",
)


def get_not_found_http_exeption(name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{name} not found",
    )


def get_already_exists_http_exeption(name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=name,
    )
