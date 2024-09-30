from aiohttp import web

from app.routes import setup_routes


async def create_app():
    app = web.Application()
    setup_routes(app)
    return app

