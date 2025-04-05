from fastapi import FastAPI, HTTPException
from models import Todo, TodoCreate, TodoUpdate
from typing import List


app = FastAPI()

all_todos = [
    Todo(id=1, description='Go outside', priority=1),
    Todo(id=2, description='Study for fun', priority=1),
    Todo(id=3, description='Watch "Wheel of Time"', priority=3),
    Todo(id=4, description='Go to the gym', priority=2),
    Todo(id=5, description='Hope for the best', priority=1),
]


@app.get('/', response_model=dict)
async def root():
    return {'message': 'Welcome to Todo list application!'}


@app.get('/todos', response_model=List[Todo])
async def get_todos():
    """
    Return all existing todo entries
    """
    return all_todos


@app.get('/todos/{todo_id}', response_model=Todo)
async def get_todo_item(todo_id: int):
    """
    Return todo entry by id
    """
    for item in all_todos:
        if item.id == todo_id:
            return item
    return HTTPException(status_code=404, detail='Item not found')


@app.post('/todos', response_model=Todo)
async def create_todo_item(todo: TodoCreate):  # connect to pydantic validation
    """
    Create a todo entry
    """
    new_id = all_todos[-1].id + 1 if all_todos else 1
    new_todo = Todo(id=new_id, description=todo.description, priority=todo.priority)
    all_todos.append(new_todo)
    return new_todo


@app.put('/todos/{todo_id}', response_model=Todo)
async def update_todo_item(todo_id: int, todo: TodoUpdate):
    """
    Update todo entry (overwrite with new data)
    """
    for item in all_todos:
        if item.id == todo_id:
            item.description = (todo.description or item.description)
            item.priority = (todo.priority or item.priority)
            return item
    return HTTPException(status_code=404, detail='Item not found')


@app.delete('/todos/{todo_id}', response_model=dict)
async def delete_todo_item(todo_id: int):
    """
    Delete todo entry
    """
    for item in all_todos:
        if item.id == todo_id:
            all_todos.remove(item)
            return {'message': f'Item with id {todo_id} is removed'}
    return HTTPException(status_code=404, detail='Item not found')
