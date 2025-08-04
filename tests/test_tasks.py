import pytest


@pytest.mark.asyncio
async def test_create_task(client, token):
	response = await client.post("tasks/", json={
		"title": "test task",
		"description": "DESC"
	}, headers={
		"Authorization": f"Bearer {token}"
	})

	assert response.status_code == 200
	assert response.json()['title'] == "test task"


@pytest.mark.asyncio
async def test_get_all_tasks(client, token):
	response = await client.get('tasks/', headers={
		'Authorization': f"Bearer {token}"
	})
	result = response.json()
	assert 200 == response.status_code
	assert len(result) > 0


@pytest.mark.asyncio
async def test_get_by_id(client, token):
	response = await client.post("tasks/", json={
		"title": "test task11",
		"description": "DESC"
	}, headers={
		"Authorization": f"Bearer {token}"
	})
	id = response.json()['id']
	response = await client.get(f"tasks/{id}", headers={
		"Authorization": f"Bearer {token}"
	})
	assert 200 == response.status_code
	assert 'test task11' == response.json()['title']


@pytest.mark.asyncio
async def test_update_task(client, token):
	response = await client.get('tasks/', headers={
		'Authorization': f"Bearer {token}"
	})
	result = response.json()
	assert 200 == response.status_code
	assert len(result) > 0
	assert False == result[0]['is_completed']

	id = result[0]['id']
	response = await client.patch(f"tasks/{id}", json={
		'is_completed': True
	}, headers={
		"Authorization": f"Bearer {token}"
	})

	result = response.json()

	assert 200 == response.status_code
	assert result['id'] == id
	assert True == result['is_completed']

@pytest.mark.asyncio
async def test_delete_task(client, token):
    # Получаем все задачи
    response = await client.get("tasks/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0

    # Берем ID первой задачи
    task_id = tasks[0]['id']

    # Удаляем задачу
    response = await client.delete(f"tasks/{task_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

    # Пробуем получить удаленную задачу
    response = await client.get(f"tasks/{task_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404