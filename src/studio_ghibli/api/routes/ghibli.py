
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from studio_ghibli.api.dependencies import CurrentUser, HttpClientDep
from studio_ghibli.models.user import UserTable
from studio_ghibli.schemas.ghibli import GhibliResource
from studio_ghibli.schemas.user import UserRole
from studio_ghibli.services.ghibli_service import fetch_ghibli_data


router = APIRouter(prefix="/ghibli", tags=["ghibli"])

def check_resource_access(
    user: UserTable,
    resource: GhibliResource
) -> None:
  if user.role != UserRole.admin and user.role.value != resource.value:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Your role cannot access this Ghibli resource"
    )

@router.get("/{resource}", response_model=None)
async def get_collection(
  resource: GhibliResource,
  current_user: CurrentUser,
  client: HttpClientDep
) -> Any:
  check_resource_access(current_user,resource)
  return await fetch_ghibli_data(client, resource)

@router.get("/{resource}/{item_id}", response_model=None)
async def get_item_from_collection(
  resource: GhibliResource,
  item_id: UUID,
  current_user: CurrentUser,
  client: HttpClientDep
) -> Any:
  check_resource_access(current_user,resource)
  return await fetch_ghibli_data(client, resource, str(item_id))
