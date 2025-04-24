import uuid

from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    uid: str = Field(
        primary_key=True, unique=True, default_factory=lambda: str(uuid.uuid4())
    )
    description: str
    priority: int = Field(default=3)

    def __repr__(self):
        return f"<Todo {self.description}>"
