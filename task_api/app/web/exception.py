from fastapi import HTTPException, status


UNAUTHORIZE = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid email or password", 
            headers={"WWW-Authenticate": "Bearer"})

INVALID_DATA = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data for writing")

FORBIDDEN = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User has blocked or not confirmed email")