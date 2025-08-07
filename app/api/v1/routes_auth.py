from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.db.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token, hash_password
from app.schemas.user import Token, UserCreate, UserOut


router = APIRouter()

@router.post('/register', response_model=UserOut)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
	user = await UserRepository.get_by_email(db, user_data.email)
	if user:
		raise HTTPException(status_code=400, detail="Email is already used")

	new_user = await UserRepository.create(db, user_data)
	return new_user


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_session)):
	user = await UserRepository.get_by_email(db, form_data.username)
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=400, detail="Wrong email or password")

	token = create_access_token({"sub": str(user.id)})
	return Token(access_token=token)