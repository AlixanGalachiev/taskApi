from app.core.dependencies import get_current_user
from app.db.models.user import User
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.db.repositories.task_repository import TaskRepository
# from app.db.repositories.user_repository import UserRepository
from app.schemas.task import *

router = APIRouter()

@router.post('/')
async def create(
	task_data: TaskCreate,
	db: AsyncSession = Depends(get_session),
	current_user: User =  Depends(get_current_user)
):
	return await TaskRepository.create(db, task_data, current_user.id)


@router.get('/')
async def get_all(
	db: AsyncSession = Depends(get_session),
	current_user: User = Depends(get_current_user)
):
	return await TaskRepository.get_all_by_owner_id(db, current_user.id)
	

@router.get('/{id}')
async def get_by_di(
	id: int,
	db: AsyncSession = Depends(get_session),
	current_user: User = Depends(get_current_user)
):
	task = await TaskRepository.get_by_id(db, id, current_user.id)
	if not task:
		raise HTTPException(status_code=404, detail="Task not found")
	return task


@router.patch('/{id}')
async def update(
	id: int,
	updates: TaskUpdate,
	db: AsyncSession = Depends(get_session),
	current_user: User = Depends(get_current_user)
):
	task = await TaskRepository.get_by_id(db, id, current_user.id)
	if not task:
		raise HTTPException(status_code=404, detail="Task not found")
	task = await TaskRepository.update(db, task, updates)
	return task


@router.delete("/{id}")
async def delete(
	id: int,
	db: AsyncSession = Depends(get_session),
	current_user: User = Depends(get_current_user)
):
	return True