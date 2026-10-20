from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    admin = "admin"
    films = "films"
    people = "people"
    locations = "locations"
    species = "species"
    vehicles = "vehicles"



class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: UserRole


class UserRead(BaseModel):
    id: UUID
    name: str
    role: UserRole

class UserUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: UserRole

