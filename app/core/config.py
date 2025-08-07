import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	ENV: str = "dev"

	DB_HOST: str
	DB_PORT: str
	DB_USER: str
	DB_PASS: str
	DB_NAME: str

	JWT_AUTH_KEY: str

	class Config:
		# Динамически выбираем .env-файл в зависимости от переменной ENV
		env_file = f".env.{os.getenv('ENV', 'dev')}"
		env_file_encoding = 'utf-8'


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


@lru_cache()
def get_settings():
	return Settings()

settings = get_settings()
