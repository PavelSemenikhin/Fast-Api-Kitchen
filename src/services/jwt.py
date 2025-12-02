import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from starlette import status

from core.config import settings


ALGORITHM = "HS256"
EXPIRATION_TIME_ACCESS = 30  # minutes
EXPIRATION_TIME_REFRESH = 60  # days


def create_access_token(
    data: dict, expires_minutes: int = EXPIRATION_TIME_ACCESS
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(to_encode, settings.jwt.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict, expires_days: int = EXPIRATION_TIME_REFRESH
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode, settings.jwt.refresh_secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt.secret_key,
            algorithms=[ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt.refresh_secret_key,
            algorithms=[ALGORITHM],
        )

        if not payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token payload",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type",
            )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
