from fastapi import FastAPI

from src_db.routes import todo_router
from src_db.db.main import lifespan

base_url = '/todos'

app = FastAPI(lifespan=lifespan)
app.include_router(todo_router, prefix=base_url)
