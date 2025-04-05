from pydantic import BaseModel, Field
from typing import Optional
from enum import IntEnum


class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class TodoBase(BaseModel):
    description: str = Field(..., min_length=2, max_length=512, description='description')
    priority: Priority = Field(default=Priority.LOW, description='priority')


# for create keeping setup as for Base class, since need to specify all fields during creation
class TodoCreate(TodoBase):
    pass


# for update need to have ability to update 1 field or all
class TodoUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=2, max_length=512, description='description')
    priority: Optional[Priority] = Field(None, description='priority')


class Todo(TodoBase):
    id: int = Field(..., description='unique identifier')
