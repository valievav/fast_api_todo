from typing import List

from fastapi import APIRouter, HTTPException, Depends

from .data import get_all_todos
from .schemas import Todo, TodoCreate, TodoUpdate

todo_router = APIRouter()


@todo_router.get('/', response_model=List[Todo])
async def get_todos(all_todos=Depends(get_all_todos)):
    """
    Return all existing todo entries
    """
    return all_todos


@todo_router.get('/{todo_id}', response_model=Todo)
async def get_todo_item(todo_id: int, all_todos=Depends(get_all_todos)):
    """
    Return todo entry by id
    """
    for item in all_todos:
        if item.id == todo_id:
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@todo_router.post('/', response_model=Todo)
async def create_todo_item(todo: TodoCreate, all_todos=Depends(get_all_todos)):  # connect to pydantic validation
    """
    Create a todo entry
    """
    new_id = all_todos[-1].id + 1 if all_todos else 1
    new_todo = Todo(id=new_id, description=todo.description, priority=todo.priority)
    all_todos.append(new_todo)
    return new_todo


@todo_router.put('/{todo_id}', response_model=Todo)
async def update_todo_item(todo_id: int, todo: TodoUpdate, all_todos=Depends(get_all_todos)):
    """
    Update todo entry (overwrite with new data)
    """
    for item in all_todos:
        if item.id == todo_id:
            item.description = (todo.description or item.description)
            item.priority = (todo.priority or item.priority)
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@todo_router.delete('/{todo_id}', response_model=dict)
async def delete_todo_item(todo_id: int, all_todos=Depends(get_all_todos)):
    """
    Delete todo entry
    """
    for item in all_todos:
        if item.id == todo_id:
            all_todos.remove(item)
            return {'message': f'Item with id {todo_id} is removed'}
    raise HTTPException(status_code=404, detail='Item not found')
