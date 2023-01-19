from fastapi import FastAPI, Depends

from common.config.consts import AUTH_HEADER

from search.routes import search


def include_routers(app: FastAPI):
    app.include_router(search.router, tags=['Search'], prefix='/api/v1/search')
