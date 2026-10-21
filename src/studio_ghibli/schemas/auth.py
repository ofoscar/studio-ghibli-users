from pydantic import BaseModel, Field

class Token(BaseModel):
  access_token: str
  token_type: str

class PasswordChange(BaseModel):
  current_password: str
  new_password: str = Field(min_length=12, max_length=128)