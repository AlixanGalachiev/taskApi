import pytest

base_url = "/api/v1"

@pytest.mark.asyncio
async def test_create_task(client):
	login = await client.post(base_url + "/auth/login", data={
		"username": "test@example.com",
		"password": "2345"
	})
	token = login.json()['access_token']


	response = await client.post(f"{base_url}/tasks/", json={
		"title": "test task",
		"description": "DESC"
	}, headers={
		"Authorization": f"Bearer {token}"
	})

	assert response.status_code == 200
	assert response.json()['title'] == "test task"