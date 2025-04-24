from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src_db.db.main import get_session
from .schemas import TodoSchema, TodoCreate, TodoUpdate
from .service import TodoService

todo_router = APIRouter()
todo_service = TodoService()


@todo_router.get('/', response_model=List[TodoSchema])
async def get_todos(session: AsyncSession = Depends(get_session)):
    """
    Return all existing todo entries
    """
    all_todos = await todo_service.get_all_todos(session)
    return all_todos


@todo_router.get('/{todo_uid}', response_model=TodoSchema)
async def get_todo_item(todo_uid: str, session: AsyncSession = Depends(get_session)):
    """
    Return todo entry by uid
    """
    todo = await todo_service.get_todo(todo_uid, session)
    if todo:
        return todo

    raise HTTPException(status_code=404, detail='Item not found')


@todo_router.post('/', response_model=TodoSchema)
async def create_todo_item(todo: TodoCreate, session: AsyncSession = Depends(get_session)):  # connect to pydantic validation
    """
    Create a todo entry
    """
    new_todo = await todo_service.create_todo(todo, session)
    return new_todo


@todo_router.put('/{todo_uid}', response_model=TodoSchema)
async def update_todo_item(todo_uid: str, todo: TodoUpdate, session: AsyncSession = Depends(get_session)):
    """
    Update todo entry (overwrite with new data)
    """
    updated_todo = await todo_service.update_todo(todo_uid, todo, session)
    if updated_todo:
        return updated_todo

    raise HTTPException(status_code=404, detail='Item not found')


@todo_router.delete('/{todo_uid}', response_model=dict)
async def delete_todo_item(todo_uid: str, session: AsyncSession = Depends(get_session)):
    """
    Delete todo entry
    """
    result = await todo_service.delete_todo(todo_uid, session)
    if result:
        return  {'message': f'Item with id {todo_uid} is removed'}

    raise HTTPException(status_code=404, detail='Item not found')
