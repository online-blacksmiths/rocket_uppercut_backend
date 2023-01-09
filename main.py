import uvicorn
from dataclasses import asdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from common.config.settings import conf
from common.config.rdb_conn import rdb
from common.config.mongodb_conn import mongodb

from common.utils.middlewares import request_middleware

from common.routes import index


def create_app():
    app = FastAPI()

    # RDB Connect
    rdb.init_app(app, **asdict(conf()))

    # MongoDB Connect
    mongodb()

    # Middleware
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=request_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Endpoint
    app.include_router(index.router, tags=['Health Check'], deprecated=True)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=conf().PORT, reload=True)
