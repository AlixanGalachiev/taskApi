from app.db.models.user import User
from app.db.session import get_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repository import UserRepository
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)) -> User:
	payload = decode_access_token(token)
	if not payload or "sub" not in payload:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
	user = await UserRepository.get_by_id(db, int(payload["sub"]))

	if not user:
		raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="User not found")

	return user

