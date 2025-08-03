from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

class UserRepository:
	@staticmethod
	async def create(db: AsyncSession, task_data: UserCreate):
		user = User(**task_data)
		db.add(user)
		db.commit()
		db.refresh(user)
		return user


	@staticmethod
	async def get_by_id(db: AsyncSession, id: int):
		result = await db.execute(select(User).where(User.id ==id))
		return result.scalars().first()


	@staticmethod
	async def update(db: AsyncSession, user: User, updates: UserUpdate):
		for key, value in updates.dict(exclude_unset=True).items():
			setattr(user, key, value)
			await db.commit()
			await db.refresh(user)
		return user


	@staticmethod
	async def delete(db: AsyncSession, id: int):
		stmt = delete(User).where(User.id == id)
		await db.execute(stmt)
		await db.commit()