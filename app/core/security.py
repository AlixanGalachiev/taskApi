from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
	return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta|None = None):
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
	to_encode.update({'exp': expire})
	return jwt.encode(to_encode, settings.JWT_AUTH_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_AUTH_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None