from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	DB_HOST: str
	DB_PORT: int
	DB_USER: str
	DB_PASS: str
	DB_NAME: str

	@property
	def DATABASE_URL(self) -> str:
		return (
			f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
			f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
		)

	@property
	def DATABASE_URL_SYNC(self) -> str:
		return (
			f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
			f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
		)

	class Config:
		env_file = ".env"

@lru_cache()
def get_settings():
	return Settings()

settings = get_settings()
