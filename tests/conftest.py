import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_session

from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

@pytest_asyncio.fixture
async def test_db():
	engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
	async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
	yield async_session
 
	await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db):
	async def override_get_sesion():
		async with test_db() as session:
			yield session

	app.dependency_overrides[get_session] = override_get_sesion
	async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1/") as ac:
		yield ac


@pytest_asyncio.fixture
async def token(client):
	login = await client.post("/auth/login", data={
		"username": "test@example.com",
		"password": "2345"
	})

	return login.json()['access_token']
