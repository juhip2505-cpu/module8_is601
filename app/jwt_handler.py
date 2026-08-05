from typing import Annotated
import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "module13-development-secret-key",
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        return None


def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = (
        db.query(User)
        .filter(User.id == int(payload["sub"]))
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user