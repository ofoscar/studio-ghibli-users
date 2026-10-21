from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from studio_ghibli.core.config import settings
from studio_ghibli.core.database import get_session
from studio_ghibli.core.security import ALGORITHM
from studio_ghibli.models.user import UserTable
from studio_ghibli.schemas.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
SessionDep = Annotated[Session, Depends(get_session)]

credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> UserTable:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[ALGORITHM],
        )
        subject = payload.get("sub")
        user_id = UUID(subject)
    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_error

    user = session.get(UserTable, user_id)
    if user is None:
        raise credentials_error

    return user


CurrentUser = Annotated[UserTable, Depends(get_current_user)]


def require_admin(current_user: CurrentUser) -> UserTable:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return current_user