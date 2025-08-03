from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
	email: str
	password: str

class UserCreate(UserBase):
	pass

class UserUpdate(UserBase):
	email: str | None = None
	is_active: bool | None = None
	is_admin: bool | None = None

class UserInDB(UserBase):

	id: int
	is_active: bool
	is_admin: bool

	tasks: list[int]

	class Config:
		from_attributes = True
