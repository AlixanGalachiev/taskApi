from app.db.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
class TaskRepository:

	@staticmethod
	async def create(db: AsyncSession, task_data: TaskCreate, owner_id: int):
		task = Task(**task_data.dict(), owner_id = owner_id)
		db.add(task)
		await db.commit()
		await db.refresh(task)
		return task


	@staticmethod
	async def get_all_by_owner_id(db: AsyncSession, owner_id: int):
		result = await db.execute(select(Task).where(Task.owner_id == owner_id))
		return result.scalars().all()


	@staticmethod
	async def get_by_id(db: AsyncSession, id: int, owner_id: int):
		result = await db.execute(select(Task).where(Task.id == id, Task.owner_id == owner_id))
		return result.scalars().first()


	@staticmethod
	async def update(db: AsyncSession, task: Task, updates: TaskUpdate):
		for key, value in updates.dict(exclude_unset=True).items():
			setattr(task, key, value)
		await db.commit()
		await db.refresh(task)
		return task


	@staticmethod
	async def delete(db: AsyncSession, id: int):
		stmt = delete(Task).where(Task.id == id)
		await db.execute(stmt)
		await db.commit()