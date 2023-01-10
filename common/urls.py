from fastapi import FastAPI

from common.routes import index


def include_routers(app: FastAPI):
    app.include_router(index.router, tags=['ETC'], deprecated=True)
