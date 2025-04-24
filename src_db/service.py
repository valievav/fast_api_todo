from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src_db.db.models import Todo
from .schemas import TodoCreate, TodoUpdate


class TodoService:
    async def get_all_todos(self, session: AsyncSession):
        statement = select(Todo).order_by(desc(Todo.priority))
        result = await session.exec(statement)
        return result.all()

    async def get_todo(self, todo_uid: str, session: AsyncSession):
        statement = select(Todo).where(Todo.uid == todo_uid)
        result = await session.exec(statement)
        todo = result.first()
        return None or todo

    async def create_todo(self, todo_data: TodoCreate, session: AsyncSession):
        todo_data_dict = todo_data.model_dump()
        new_todo = Todo(**todo_data_dict)
        session.add(new_todo)

        await session.commit()
        return new_todo

    async def update_todo(self, todo_uid: str, upd_data: TodoUpdate, session: AsyncSession):
        todo_to_update = await self.get_todo(todo_uid, session)
        if not todo_to_update:
            return None

        upd_data_dict = upd_data.model_dump()
        for k, v in upd_data_dict.items():
            if v is not None:
                setattr(todo_to_update, k, v)

        await session.commit()
        return todo_to_update

    async def delete_todo(self, todo_uid: str, session: AsyncSession):
        todo_to_delete = await self.get_todo(todo_uid, session)
        if not todo_to_delete:
            return None

        await session.delete(todo_to_delete)
        await session.commit()

        return True
