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
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=12, max_length=128)
    
class UserRead(BaseModel):
    id: UUID
    name: str
    role: UserRole

class UserUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: UserRole

