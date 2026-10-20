from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlmodel import Session, select

from studio_ghibli.core.database import get_session
from studio_ghibli.models.user import UserTable
from studio_ghibli.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep) -> UserRead:
    db_user = UserTable(name=user.name, role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserRead(id=db_user.id, name= db_user.name, role=db_user.role)

@router.get("/", response_model=list[UserRead])
def get_users(
    session:SessionDep,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[UserRead]:
    statement = select(UserTable).offset(offset).limit(limit)
    db_users = session.exec(statement).all()

    return [
        UserRead(id=user.id, name=user.name, role=user.role)
        for user in db_users
    ]

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, session: SessionDep) -> UserRead:
    db_user = session.get(UserTable, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserRead(id=db_user.id, name=db_user.name, role=db_user.role)

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    user: UserUpdate,
    session: SessionDep,
) -> UserRead:
    db_user = session.get(UserTable, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_user.name = user.name
    db_user.role = user.role

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserRead(id=db_user.id, name=db_user.name, role=db_user.role)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, session: SessionDep) -> None:
    db_user = session.get(UserTable, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detai="User not found"
        )

    session.delete(db_user)
    session.commit()