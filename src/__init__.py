from fastapi import FastAPI

from src.routes import todo_router

base_url = '/todos'

app = FastAPI()
app.include_router(todo_router, prefix=base_url)
