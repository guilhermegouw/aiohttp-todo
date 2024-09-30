from aiohttp import web
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from app.db import get_db_session
from app.models import Todo


async def get_todos(request):
    async for session in get_db_session():
        result = await session.execute(select(Todo))
        todos = result.scalars().all()
        todos_list = [
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
            }
            for todo in todos
        ]
        return web.json_response(todos_list)


async def create_todo(request):
    data = await request.json()
    new_todo = Todo(
        title=data.get("title"), description=data.get("description")
    )
    async for session in get_db_session():
        session.add(new_todo)
        await session.commit()
        return web.json_response(
            {"id": new_todo.id, "message": "Todo created successfully"}
        )


async def get_todo(request):
    try:
        todo_id = int(request.match_info["id"])
    except ValueError:
        return web.json_response({"error": "Invalid todo ID"}, status=400)

    async for session in get_db_session():
        try:
            todo = await session.get(Todo, todo_id)
            if todo is None:
                raise NoResultFound
            return web.json_response(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                }
            )
        except NoResultFound:
            return web.json_response({"error": "Todo not found"})


async def update_todo(request):
    try:
        todo_id = int(request.match_info["id"])
    except ValueError:
        return web.json_response({"error": "Invalid todo ID"}, status=400)

    data = await request.json()

    async for session in get_db_session():
        todo = await session.get(Todo, todo_id)

        if not todo:
            return web.json_response({"error": "Todo not found"}, status=404)

        todo.title = data.get("title", todo.title)
        todo.description = data.get("description", todo.description)
        todo.completed = data.get("completed", todo.completed)
        await session.commit()
        return web.json_response({"message": "Todo updated successfully"})


async def delete_todo(request):
    try:
        todo_id = int(request.match_info["id"])
    except ValueError:
        return web.json_response({"error": "Invalid todo ID"}, status=400)

    async for session in get_db_session():
        todo = await session.get(Todo, todo_id)

        if not todo:
            return web.json_response({"error": "Todo not found"}, status=404)

        await session.delete(todo)
        await session.commit()
        return web.json_response({"message": "Todo deleted successfully"})
