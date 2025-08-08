import pytest

@pytest.mark.asyncio
async def test_registration(client):
	response = await client.post(f"{base_url}/auth/register", json={
		"email": "test@example.com",
		"password": "2345"
	})

	assert response == 1
	

@pytest.mark.asyncio
async def test_login(client):
	response = await client.post("/auth/login", data={
		"username": "test@example.com",
		"password": "2345"
	})
	assert response.status_code == 200
	assert 'access_token' in response.json()
