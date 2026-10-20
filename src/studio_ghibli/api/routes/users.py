from uuid import UUID, uuid4

from fastapi import APIRouter, Query, status, HTTPException

from studio_ghibli.schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

_users: dict[UUID, UserRead] = {}

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> UserRead:
    new_user = UserRead(
        id=uuid4(),
        name=user.name,
        role=user.role,
    )
    _users[new_user.id] = new_user
    return new_user

@router.get("/", response_model=list[UserRead])
def get_users(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[UserRead]:
    users = list(_users.values())
    return users[offset : offset + limit]

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID) -> UserRead:
    user = _users.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user