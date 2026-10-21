from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from studio_ghibli.api.dependencies import CurrentUser
from studio_ghibli.core.database import get_session
from studio_ghibli.core.security import create_access_token, hash_password, verify_password
from studio_ghibli.models.user import UserTable
from studio_ghibli.schemas.auth import PasswordChange, Token

router = APIRouter(prefix="/auth", tags=["auth"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/token", response_model=Token)
def login(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  session: SessionDep
) -> Token:
  statement = select(UserTable).where(
    UserTable.username == form_data.username
  )
  user = session.exec(statement).first()

  if (
    user is None
    or user.password_hash is None
    or not verify_password(form_data.password, user.password_hash)
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"}
    )

  token = create_access_token(subject=str(user.id))
  return Token(access_token=token, token_type="bearer")

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
  passwords: PasswordChange,
  current_user: CurrentUser,
  session: SessionDep
) -> None:
  if current_user.password_hash is None or not verify_password(
    passwords.current_password, current_user.password_hash
  ):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Current password is incorrect"
  )

  current_user.password_hash = hash_password(passwords.new_password)
  session.add(current_user)

  session.commit()
