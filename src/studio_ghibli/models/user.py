from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from studio_ghibli.schemas.user import UserRole

class UserTable(SQLModel, table=True):
  id: UUID = Field(default_factory=uuid4,primary_key=True)
  name: str = Field(max_length=100)
  role: UserRole