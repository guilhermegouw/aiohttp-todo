from aiohttp import web

from app.views import (create_todo, delete_todo, get_todo, get_todos,
                       update_todo)


def setup_routes(app):
    app.router.add_get("/todos", get_todos)
    app.router.add_post("/todos", create_todo)
    app.router.add_get("/todos/{id}", get_todo)
    app.router.add_put("/todos/{id}", update_todo)
    app.router.add_delete("/todos/{id}", delete_todo)
