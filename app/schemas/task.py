from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
	title: str
	description: Optional[str] = None

class TaskCreate(TaskBase):
	pass

class TaskUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	is_completed: Optional[bool] = None

class TaskInDB(TaskBase):
	id: int
	is_completed: bool
	owner_id: int

	class Config:
		from_attributes = True
