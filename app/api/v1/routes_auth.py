from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.db.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.user import Token, UserCreate, UserOut


router = APIRouter()

@router.post('/register', response_model=UserOut)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
	user = await UserRepository.get_by_email(db, user_data.email)
	print(123)
	if user:
		raise HTTPException(status_code=400, detail="Email is already used")
	print(123)
	new_user = await UserRepository.create(db, user_data)
	print(123)
	return new_user


@router.post('/login', response_model=Token)
async def login(user_data: UserCreate, db: AsyncSession=Depends(get_session)):
	user = await UserRepository.get_by_email(db, user_data.email)
	if not user or not verify_password(user_data.password, user.hashed_password):
		raise HTTPException(status_code=400, detail="Wrong email or password")
	token = create_access_token({"sub": str(user.id)})
	return Token(access_token=token)