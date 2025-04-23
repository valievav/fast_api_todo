from fastapi import FastAPI

from src.routes import todo_router

app = FastAPI()
app.include_router(todo_router, prefix='')
