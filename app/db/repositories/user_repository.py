from app.core.security import hash_password
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import EmailStr

class UserRepository:
	@staticmethod
	async def create(db: AsyncSession, user_data: UserCreate):
		print(user_data)
		user = User(email=user_data.email, hashed_password=hash_password(user_data.password))
		db.add(user)
		await db.commit()
		await db.refresh(user)
		return user


	@staticmethod
	async def get_by_id(db: AsyncSession, id: int):
		result = await db.execute(select(User).where(User.id ==id))
		return result.scalars().first()

	@staticmethod
	async def get_by_email(db: AsyncSession, email: EmailStr):
		result = await db.execute(select(User).where(User.email==email))
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